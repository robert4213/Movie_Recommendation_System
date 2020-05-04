@ECHO OFF

FOR %%a in (2,4,6,8,10,15,20,40) do (
    FOR %%b in (5,10,20,30,50) DO (
        python train.py %%a %%b
    )
)

PAUSE