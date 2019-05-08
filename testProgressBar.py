import time
from organisation_functions import UpdateProgress

# UpdateProgress test script
print('progress : "Hello"')
UpdateProgress('Hello')
time.sleep(1)

print()
print('progress : 3')
UpdateProgress(3)
time.sleep(1)

print()
print('progress : [23]')
UpdateProgress([23])
time.sleep(1)

print()
print('progress : -10')
UpdateProgress(-10)
time.sleep(2)

print()
print('progress : 10')
UpdateProgress(10)
time.sleep(2)

print()
print('progress : 0->1')
for i in range(101):
    time.sleep(0.1)
    UpdateProgress(i/100.0)

print()
print('Test completed')
