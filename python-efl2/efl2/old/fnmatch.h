/*
 * Definitions for fnmatch, copy+pasted from <fnmatch.h> with some small
 * cleanups by hand.
 */

/* Bits set in the FLAGS argument to `fnmatch'.  */
#define	FNM_PATHNAME	... 
#define	FNM_NOESCAPE	... 
#define	FNM_PERIOD	... 

/* Value returned by `fnmatch' if STRING does not match PATTERN.  */
#define	FNM_NOMATCH	1

/* Match NAME against the filename pattern PATTERN,
   returning zero if it matches, FNM_NOMATCH if not.  */
extern int fnmatch (const char *__pattern, const char *__name, int __flags);

