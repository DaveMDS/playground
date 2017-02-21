
#include <stdio.h>      /* printf */
#include <string.h>     /* strcat */
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <sched.h>
#include <sys/time.h>

// #include <wiringPi.h>
// #include <wiringPiSPI.h>


#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>


typedef enum { false, true } bool;

void print_binary(uint8_t n)
{
	char buf[9];
	int i;

	buf[0] = '\0';

	for (i = 128; i > 0; i >>= 1)
		strcat(buf, ((n & i) == i) ? "1" : "0");

	printf("%s ", buf);
}

typedef struct {
	uint8_t r;
	uint8_t g;
	uint8_t b;
}RGB;

RGB PALETTE[] = {
	{ 0, 0, 0 },		//  0  // black
	{ 1, 0, 0 },		//  1  // red
	{ 0, 1, 0 },		//  2  // green
	{ 0, 0, 1 },		//  3  // blue
	{ 1, 1, 1 },		//  4  // white
	{ 1, 1, 0 },		//  5  // yellow
	{ 1, 0, 1 },		//  6  // magenta
	{ 0, 1, 1 },		//  7  // cyan
};

#define SPI_DEVICE "/dev/spidev0.0"
#define NUM_LEDS 8
#define NUM_SHIFT_REGS 3 // not counting the last one for the levels

uint8_t FRAME[NUM_LEDS] = { 1,2,3,4,5,6,7,0 };

uint8_t BUFFER[NUM_SHIFT_REGS + 1]; // counting the last one (in pos [0])

static int spifd;

void
buffer_clear(void)
{
	printf("Buffer clear\n");
	// set all the buffer to 0x11111111 (all led off)
	// ...ignoring the first shift register (used for the levels)
	memset(BUFFER + 1, 0xFF, NUM_SHIFT_REGS);
}

void
buffer_prepare(uint8_t *frame)
{
	uint8_t shift_register, bit;
	int led_num;
	RGB color;

	// printf("Buffer prepare\n");

	// Here we WILL set the level selector byte (current level)
	BUFFER[0] = 0b00000000;

	// Example: only first led red:
	// BUFFER[0] = 0b11111111;
	// BUFFER[1] = 0b11111111;
	// BUFFER[N] = 0b11111110;

	bit = 0;
	shift_register = NUM_SHIFT_REGS; // not touching the level selector
	for (led_num = 0; led_num < NUM_LEDS; led_num++)
	{
		color = PALETTE[frame[led_num]];
		// printf("Led %d: %d %d %d :: byte: %d  bit: %d\n", led_num, color.r, color.g, color.b, shift_register, bit);

		// red
		if (color.r > 0)
			BUFFER[shift_register] &= ~(1 << bit); // led on (0)
		else
			BUFFER[shift_register] |= (1 << bit);  // led off (1)
		if (++bit > 7) { bit = 0; shift_register --; }

		// green
		if (color.g > 0)
			BUFFER[shift_register] &= ~(1 << bit); // led on (0)
		else
			BUFFER[shift_register] |= (1 << bit);  // led off (1)
		if (++bit > 7) { bit = 0; shift_register --; }

		// blue
		if (color.b > 0)
			BUFFER[shift_register] &= ~(1 << bit); // led on (0)
		else
			BUFFER[shift_register] |= (1 << bit);  // led off (1)
		if (++bit > 7) { bit = 0; shift_register --; }
	}

	// printf("BUFFER: ");
	// print_binary(BUFFER[0]);
	// print_binary(BUFFER[1]);
	// print_binary(BUFFER[2]);
	// print_binary(BUFFER[3]);
	// printf("\n");

}

void
buffer_push(void)
{
	// printf("Buffer push\n");
	write(spifd, &BUFFER, sizeof(BUFFER));
}

int main(void)
{
	/* Try to increase the process priority */
	struct sched_param sp;
	sp.sched_priority = sched_get_priority_max(SCHED_FIFO);
	sched_setscheduler(0, SCHED_FIFO, &sp);


	// Open SPI device
	if ((spifd = open(SPI_DEVICE, O_WRONLY)) < 0)
	{
		printf("ERROR: Can't open SPI device\n");
		return 1;
	}
	printf("spi OK (%d)\n", spifd);


	buffer_clear();
	buffer_push();


	// half a second (500millis)
	#define FRAMETIME (500 * 1000) // microseconds

	// 30fps (counting 8 levels switching)
	// #define FRAMETIME (((1.0 / 30) * 1000 * 1000) / 8) // microseconds

	struct timeval loop_start, loop_end;
	int worked, elapsed;
	for (;;)
	{
		/* LOOP: keep track of start time */
		gettimeofday(&loop_start, NULL);


		buffer_prepare(FRAME);
		buffer_push();


		/* LOOP: sleep to fulfill/respect precise FRAMETIME */
		gettimeofday(&loop_end, NULL);
		worked = (loop_end.tv_sec - loop_start.tv_sec) * 1000000ULL +
			 (loop_end.tv_usec - loop_start.tv_usec);
		if (worked < FRAMETIME) {
			usleep(FRAMETIME - worked); // microseconds
		}
		else {
			printf("AAARGH! Out of time !\n");
		}

		/* LOOP: print out total frame time (only for DEBUG) */
		gettimeofday(&loop_end, NULL);
		elapsed = (loop_end.tv_sec - loop_start.tv_sec) * 1000000ULL +
			  (loop_end.tv_usec - loop_start.tv_usec);
		printf("Frame Time: %d micros (worked: %d) %.2f%% busy\n",
			elapsed, worked, (float)worked / (float)elapsed * 100);
		
	}

	close(spifd);
	return 0;
}

