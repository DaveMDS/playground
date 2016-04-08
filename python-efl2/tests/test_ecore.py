
from efl2 import ecore
# from efl2.ecore import Timer


print("starting ecore ml :)")

# def mycb(*args, **kargs):
    # print(args, kargs)
    # print(" \o/ " * 60)
    # ecore.main_loop_quit()
    # return ecore.ECORE_CALLBACK_CANCEL
# 
# def mycb2():
    # print("t")
    # return ecore.ECORE_CALLBACK_RENEW

# t = Timer(5.0, mycb, 567, asd='AsD')
# t2 = Timer(1.0, mycb2)

ml = ecore.Ecore_Mainloop()
print(ml)
ml.begin()
