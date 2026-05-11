# E Orbit User Manual

> **OCR method:** ocrmypdf  
> **Confidence:** 92.0%  
> **Generated:** 2026-05-11 08:47 UTC

---

## Smart Lock Manual

One.Specification parameters

## Specification Parameters

one

## Comparison Mode

two

## Self Learning Capacitive Press

fingerprint head
three

## Acquisition Head Resolution

508dpi
four

## Rejection Rate

<0.1%
five

## Fake Admission Rate

<0.001%
six

## Fingerprint Collection Range

+180°
seven

## Card Type

eight
user capacity
Total capacity of 250 sets: up
to 100 fingerprints, up to 100
passwords, up to 50 faces, and
up to 100 cards. Administrator

## Id Range 010-249

nine

## Scroll 600 Strip

ten

## Number Of Door Openings

greater than or equal 3000
times
eleven
working voltage
7.0V~8.4V, low voltage alarm
voltage 6.8 + 0.2V
twelve

## Dynamic Power

less than or equal 1A (no
consumption
motor action, no playback
sound
thirteen

## Static Power

less than or equal 200UA (averconsumption
age power consumption
fourteen

## Verification Time

less than or equal 3s, (including
the entire process of fingerprint collection, comparison,
and unlocking signal output
fifteen
keyboard type

## Touch Sensing

sixteen
(OLED display screen
0.96"

## Oled

seventeen

## Extemal Emergency Power Supply Fr Display Screen

5V1A Micro USB
eighteen

## Antistatic Ability

28KV (contact) >
15KV(Non-contact type)
nineteen
storage temperature
-25°C ~ 80°C
twenty
operation temperature
-25°C ~ 70°C
twenty-one
ambient humidity

## 15%Rh~ 93%Rh

Two.Setting Description
1.initialization
Long press the settings button for 5 seconds, and the voice will broadcast: "Factory reset, NO(*) YES(#)." Press
the # key to confirm, and the system will restart to its initial state.
In the initial state, any face, fingerprint, password, or card can unlock the device. Performing a factory reset
operation cannot clear the set door-opening direction or torque parameters.
> ⚠️ 2.Low battery warning
If the system's battery level is less than 25%, the system will voice prompt "Low power" ,The battery can still
be unlocked about 50 times, but please charge it in a timely manner (or replace the battery).
3.External USB emergency power supply
Using USB emergency power supply, it takes approximately 30 seconds to unlock.
4.Illegal user alarm
Failed to unlock after 3 to 5 consecutive inputs, with voice message: ‘Illegal user, illegal intrusion, owner notified’. After the 5th broadcast, the system is locked for 90 seconds, during which time no user action is taken.
Unlock after 90 seconds.
5.Virtual password
When using a password to unlock, any number can be added before and after the correct password, which
can increase the security of the digital password. For example, if the password is "123456", you can enter
"426123456745" to unlock.
> ⚠️ Note: The system can only recognize the first 16 digits
6.version number
Enter 999 # to read the system version number.
Three.Function and operation

## Wake Up Touch Panel

Press the *+# keys
Voice announcement: "Please
enter a 6 to 8 digit passAfter successful addition, voice
broadcast:: “User OOOAdd Suc-
word” (enter password)
al
1.Add User

## Please Enter The Password,

voice broadcast: "User * * *,
fingerprint, or card you want fia
to add
1.Add User
MS
1.Add Admin
Add Success”
can be added
continuously
2.Add user
+ Face: The voice will say "Enroll face." The user needs to position their face parallel to the camera at a distance of 30-80cm. Follow the voice prompts to complete the continuous face recording.
- Fingerprint: The user places their finger on the fingerprint sensor, and the voice prompts "Press again." The
user then places the same finger on the sensor to complete the continuous fingerprint recording.
- Password: The user enters a 6 to 8-digit password and confirms it by pressing the # key.
- Card: The user brings the card close to the IC card sensing area on the touch keypad, and the system automatically reads and saves the card information.
> ⚠️ Note: Number of management users: numbered 000-009, with a total of 10 digits; Number of ordinary users:
numbers 010-249, a total of 240 characters.
2.Delete user
(1) Verify Delete
After successful verificaVoice announcement:
om, vols nomdlese
2.delete user
FE
1Verify Delete
"Please verify the user
"User * * * Delete Sucto be deleted"
cess”
Verification method:
-Fingerprint: Place the finger to be deleted on the fingerprint sensor.
-Password: Enter the password to be delete.
-Card: The IC card to be deleted is located near the sensing area of the touch keyboard.
If the user exists in the system, the voice broadcast will read: "Success"; If the user does not exist, the voice
broadcast will say "Failure".
(2) Delete by ID

## After Successful Deletion,

2.delete user
2.delete by ID
:Please enter the user
voice broadcast:"User * * *,

## Id To Be Deleted

Delete Success"
3.System settings
(1) datetime settings
Voice announcement:"Please
enter the datetime" (input
time format is: year month
hour minute)
After successful networking, voice broadcast:
"Success"
3.System
1.datetime
settings
settings
(2) Installation settings
@Door opening direction setting
3.System settings
2.Installation settings
1.Opening direction [L]
> ⚠️ Note: The direction of opening the door is in the direction of opening the lock outside the door.
@Auto-lock
3.System settings
2.Installation settings
2.Delayed lock [N]
> ⚠️ Note: Delayed locking refers to setting a fixed anti lock time. Users can choose the locking time: 10S, 15S, 20S,
30S, 60S, 1205.
@Lock settings
-Tamper Alarm
3.System
2.Installation
Tam
3.Lock settings
1.Tamper Alarm [N
settings
settings
IN]
> ⚠️ Note: After activating the anti tamper alarm, if the door lock is tampered with, the system will issue an alarm
prompt: "Illegal user, illegal intrusion, owner notified". If the device is connected to the network, it will push
alarm information to the phone.
-Motor Torque
3.System
2.Installation
mE
> e ~~ pe
> ⚠️ Note: Motor torque is specific to the strength of the motor's torque.
-Lock back time
3.System
2.Installation
3.Lock settings
4.Dwell Alert [20s]
> ⚠️ Note: Within 1 minute, if
a human body is detected for a total of 20 seconds, a stay alarm will be triggered.
The pushed network devices will not receive sound and light alarms by default.
@Face recognition settings
-Lock back time
3.System
2.Installation
4.Face recogni-
1.Auto Detect [Y]
settings
settings
tion settings
> ⚠️ Note: 1. Classification of human sensory function:
-Human body sensing [off]: The intelligent door lock will not engage in human body sensing in standby
mode.
-Human body sensing [intelligence]: The intelligent door lock will not engage in human body sensing when
the door is opened.
-Human body sensing [open]: In any state, the intelligent door lock will undergo human body sensing.
2.lf there are 10 consecutive awakenings and no facial recognition is detected, human sensing will be turned
off by default for 5 minutes.
2.-Detection distance
3.System
2.Installation
iti
2Detection distance [M
> ⚠️ Note:Detection distance[Near]: About 30~50cm; Detection distance[Medium]: 50~70cm; Detection distance[Far]: 70~80cm.
(3) Function settings
@Network configuration

## Añada

- [ ] 1. Network

## After Successful Networkty

ti a »
configuration
> | Mie Ute elere

## Es) Es

ings
NM
"Success"
(Please refer to the appendix of the manual for detailed operation of networked products).
> ⚠️ Note: The distribution function only supports one mobile phone for distribution. If you enter the networking
configuration again, the last distribution data will be automatically cleared. Users should be cautious when
operating.
@Volume
| 3.System settings |
settings

## => Mentes

settings
=> Lo
2 VolumelH]
(Dual authentication
3.System settings
3.Installation settings
- [ ] 3. Dual authentication [N]
> ⚠️ Note:Dual authenticationOnly for ordinary key unlocking, two different ordinary user keys must be verified
to successfully unlock, and administrator users can directly unlock.
(4) Factory reset

## Confirm The Restoration Of Factory

3.System
3.Installation
4, Factory

## Loam

reset, voice broadcast: "Clear sucsettings
settings
reset
cess", system restart
> ⚠️ Note: After restoring the actory reset, all user data will be cleared. Please operate with caution.
4.information inquiry
(1) User Count
Voice announcement:
se SUES
1.User Count
“Admin***
inquiry
User***"
(2) Read Records
-Inquiry by order
4.information inquiry
2.ecord inquiry
1, inquiry by order
> ⚠️ Note: Sequential query starts with the latest information and goes down. Press the 8th key to search for the
next item and the 2nd key to search for the previous item.
-Inquiry by time
4.information
2.ecord
- [ ] 2. inquiry

## Enter The Time You Want To Query

inquiry
inquiry
by time
(time is year, month, day)
To change the system language of the smart lock in its factory state:
Enter the language system: 888+
Next, enter the code:
30004 (Chinese)
30074 (Portuguese)
3015# (Italian)
30014 (English)
3008# (French)
30164 (Mongolian)
3002 (Hong Kong)
30094 (Spanish)
3017 (Uzbekistan)
3003# (Russian)
30114 (Indonesian)
3018# (Kazakh)
3004# (Vietnamese)
3012# (Thai)
3019# (Serbian)
3005# (Korean)
3013# (Hebrew)
3020# (Korean)
3006# (Arabic)
3014# (Turkish)
3022# (Japanese)
(Visitor mode
In visitor mode, users can generate time-limited passwords for limited 1 to 59 minutes, counting from the
current time, which will become invalid after the time limited.
(2)Renting mode
In short-term lease mode, users can generate valid passwords for any period of time. The validity time
must be longer than the validity time and the current time. The maximum time range cannot exceed 60
days. The generated temporary password must be entered within 24 hours after the password takes
effect. Otherwise, the password becomes invalid.
(3)Nanny mode
In nanny mode, users can set the allowable time periods for unlocking every day. The time losing efficacy
shall be later than the time taking effect. The generated password needs to be input within 24 hours, otherwise it will be invalid.
(4)Password Management
The password management function can be used to delete the time-limited passwords that are already in
effect ona lock. However, it is not possible to delete the time-limited password that takes effect within 24
hours, administrator user's password, or standard user's password. If you need to invalidate all time-limited passwords, you need to delete User 000 on the lock first, and then add it again.
appendix

## App Operation

App Store search [Smart Life] Download and sign in.
1, Add device
After entering the APP, click "+" in the upper right corner of the home page to add the device, and enter
the "Add Device" page;
- [ ] 1) Two-dimensional code distribution network
- Select [Camera&lock] and click "Video lock (Wi-Fi)" to jump to the next page.
- "Reset the device" interface, click Next, check the Scan the OR code with door lock camera,click [Next].
- Select WIFI and enter password, click [Next].
- After entering the "Reset the devica" page, keep waiting, go to the smart door lock operation, let it
enter the network mode.
- Point the QR code of the mobile phone at the camera. When the lock end plays a "stomp" prompt tone,
click "| Hear a prompt" to enter the distribution state.

## Doorbell

(Dual Band)

## Lock

(Wi-Fi)
Camera &

## Lock

(NB-loT)

## Video Lock

(Wi-Fi)
rn
ul

## Camera

DVR

## Bird Feeder

(wifi)

## Lock

(Zigbee)

## No Prompts

- [ ] 2) WIFI distribution network
- Select [Camera&lock] and click "Lock (Wi-Fi)" to jump to the next page.

## Scan The Qr Code With The Door Lock

camera

## Scan The Qr Code With The Door Lock

camera
ual
pe |

## Connecting Device

Power on the device.
01:59

## Scan

devices.
- Select WIFI and enter password, click [Next].
- "Reset the Device" interface, click Next, select [EZ Mode ].
Select 2.4 GHz Wi-Fi Network and
enter password.

## Added Successfully

- After entering the "Add device" page, keep waiting, go to the smart door lock operation, let it enter the
network mode.
- If the power distribution fails, you can select "Switch the power distribution mode" or select the hotspot
mode. Connect to the Wi-Fi hotspot starting with SmartLife, and configure the network according to the instructions of the mobile phone.
> ⚠️ Note: Some device hotspot names may be user-defined
Camera &

## Camera

(Wi-Fi)
4G Camera
(ac)

## Doorbell

(Dual Band)

## Connecting Device

Power on the device.
01:59

## (Ble)

Hz)

## Camera

DVR

## Bird Feeder

(wifi)

## Lock

Select 2.4 GHz Wi-Fi Network and
enter password.

## @ L8T-Rd

(Zigbee)

## Add Device

1 devices)
added
successfully

## Select The Status Of The Indicator Light Or

hear the beep:

## Check If The Device Has Been Reset And

the indicator is blinking quickly.
Check if it is 2.4 GHz Wi-Fi.
Verify the Wi-Fi password.

## Connect Your Mobile Phone To

the device's hotspot

## 9 Connect Your Phone To The Hotspot Shown

below:

## Y Sl-Xxxx

@ Go back and add devices.

## Go To Connect

2, Remote unlocking
- Visitors ring the doorbell, the user's
mobile phone can receive a remote
unlock request.
- Click the adaptive broadcast button
to talk to the visitor.
- Slide the release button to the right
for remote unlocking.
3, Record query

## Messages Such As Doorbell Push,

illegal user, low battery, and unlocking can be queried in the log.
- [ ] 4. Member management

## 1 Days

e Member Management

## Online/Offline Password

[o] Smart Linkage
IN
- Click [Member Management] to enter the member management page.
- Click [+] in the upper right corner to select other members.
- Enter the name of the member to be bound.
-On the Member information page, click Manage Unlock Mode.

## Ea -Ed

passwordO Unlock

## Logs

-Select the user number to be bound and click OK
> ⚠️ Note: Account number - User code generated when the door lock is added.

## Member Management

ber. Associ.

## User Details

Any
® FingerPrint

## 8 Card

card10

## O Face

5, Temporary password
- [ ] 1) One-time password

## Any Unlock With Card10

49
password0 Unlock
ud storage for up to 30

## Save

3 days. You can purchase cloud storage resources of Tuya to increa:
rage duration and capacity
50 the

## User Details

® FingerPrint
© Password

## O Face

@ Cinna nin

## User Details

Any
® FingerPrint

## O Face

Select a one-time password and click Add or the + sign in the top right corner; Click to obtain the password,
the system automatically generates a set of ten-digit password, click to complete.
The password must be used within 6 hours after it is generated. The password can only be used once within
the valid period.

## Temporary Password

© Time-timited Password

## Offline Password

@ one-time Password
© Time-timited Password
click to complete.
No valid Password.
- [ ] 2) Unlimited password
Mz
No valid Password.
Add

## Expiration Time

Learing code immediately. The clearing
11-17-2023 13:00 >
ve
and expiration time before you
can obtain the
The one-time password is obtained.
y The clearing
code isnot
displayed
in
2671847259

## Message Notification

Select an unlimited password and click Add or the + sign in the top right corner; Select effective time and implementation time; Click to obtain the password, the system automatically generates a set of ten-digit password,

## Expiration Time

diately. The
clearing
code
is not displayed
in

## Features

- Fingerprint: The user places their finger on the fingerprint sensor, and the voice prompts "Press again." The
- Password: The user enters a 6 to 8-digit password and confirms it by pressing the # key.
- Card: The user brings the card close to the IC card sensing area on the touch keypad, and the system automatically reads and saves the card information.
- 3. Dual authentication [N]
- Select [Camera&lock] and click "Video lock (Wi-Fi)" to jump to the next page.
- "Reset the device" interface, click Next, check the Scan the OR code with door lock camera,click [Next].
- Select WIFI and enter password, click [Next].
- After entering the "Reset the devica" page, keep waiting, go to the smart door lock operation, let it
- Point the QR code of the mobile phone at the camera. When the lock end plays a "stomp" prompt tone,
- Select [Camera&lock] and click "Lock (Wi-Fi)" to jump to the next page.
- "Reset the Device" interface, click Next, select [EZ Mode ].
- After entering the "Add device" page, keep waiting, go to the smart door lock operation, let it enter the
- If the power distribution fails, you can select "Switch the power distribution mode" or select the hotspot
- Visitors ring the doorbell, the user's
- Click the adaptive broadcast button
- Slide the release button to the right
- 4. Member management
- Click [Member Management] to enter the member management page.
- Click [+] in the upper right corner to select other members.
- Enter the name of the member to be bound.

## Technical Specifications

| Parameter | Value |
|---|---|
| Total capacity of 250 sets | up |
| Note | The system can only recognize the first 16 digits |
| Voice announcement | "Please |
| voice broadcast | "User * * *, |
| - Fingerprint | The user places their finger on the fingerprint sensor, and the voice prompts "Press again." The |
| - Password | The user enters a 6 to 8-digit password and confirms it by pressing the # key. |
| - Card | The user brings the card close to the IC card sensing area on the touch keypad, and the system automatically reads and saves the card information. |
| Note | Number of management users: numbered 000-009, with a total of 10 digits; Number of ordinary users: |
| -Fingerprint | Place the finger to be deleted on the fingerprint sensor. |
| -Password | Enter the password to be delete. |
| -Card | The IC card to be deleted is located near the sensing area of the touch keyboard. |
| time format is | year month |
| Note | The direction of opening the door is in the direction of opening the lock outside the door. |
| Note | Delayed locking refers to setting a fixed anti lock time. Users can choose the locking time: 10S, 15S, 20S, |
| Note | After activating the anti tamper alarm, if the door lock is tampered with, the system will issue an alarm |
| prompt | "Illegal user, illegal intrusion, owner notified". If the device is connected to the network, it will push |
| Note | Motor torque is specific to the strength of the motor's torque. |
| Note | Within 1 minute, if |
| Note | 1. Classification of human sensory function: |
| Note | The distribution function only supports one mobile phone for distribution. If you enter the networking |
| Note | After restoring the actory reset, all user data will be cleared. Please operate with caution. |
| Note | Sequential query starts with the latest information and goes down. Press the 8th key to search for the |
| Enter the language system | 888+ |
| Note | Some device hotspot names may be user-defined |
| Note | Account number - User code generated when the door lock is added. |

## Setup Steps

1. 1. Network
2. 3. Dual authentication [N]
3. 2. inquiry
4. 1) Two-dimensional code distribution network
5. 2) WIFI distribution network
6. 4. Member management
7. 1) One-time password
8. 2) Unlimited password

## App Setup

1. Using USB emergency power supply, it takes approximately 30 seconds to unlock.
2. (Please refer to the appendix of the manual for detailed operation of networked products).
3. appendix
4. APP Operation
5. App Store search [Smart Life] Download and sign in.
6. After entering the APP, click "+" in the upper right corner of the home page to add the device, and enter
7. - Select WIFI and enter password, click [Next].
8. (wifi)
9. 2) WIFI distribution network
10. More device-pairing FAQs

## Warnings & Notes

> ⚠️ 2.Low battery warning
> ⚠️ Note: The system can only recognize the first 16 digits
> ⚠️ Note: Number of management users: numbered 000-009, with a total of 10 digits; Number of ordinary users:
> ⚠️ Note: The direction of opening the door is in the direction of opening the lock outside the door.
> ⚠️ Note: Delayed locking refers to setting a fixed anti lock time. Users can choose the locking time: 10S, 15S, 20S,
> ⚠️ Note: After activating the anti tamper alarm, if the door lock is tampered with, the system will issue an alarm
> ⚠️ Note: Motor torque is specific to the strength of the motor's torque.
> ⚠️ Note: Within 1 minute, if
> ⚠️ Note: 1. Classification of human sensory function:
> ⚠️ Note:Detection distance[Near]: About 30~50cm; Detection distance[Medium]: 50~70cm; Detection distance[Far]: 70~80cm.
> ⚠️ Note: The distribution function only supports one mobile phone for distribution. If you enter the networking
> ⚠️ Note:Dual authenticationOnly for ordinary key unlocking, two different ordinary user keys must be verified
> ⚠️ Note: After restoring the actory reset, all user data will be cleared. Please operate with caution.
> ⚠️ Note: Sequential query starts with the latest information and goes down. Press the 8th key to search for the
> ⚠️ Note: Some device hotspot names may be user-defined
> ⚠️ Note: Account number - User code generated when the door lock is added.

## Troubleshooting

1. Note: After activating the anti tamper alarm, if the door lock is tampered with, the system will issue an alarm
2. Report Issue
