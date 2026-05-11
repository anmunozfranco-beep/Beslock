# e-Orbit
## Image generation matrix for DALL·E or other graphic AI

## 1. Objective
This document organizes the images needed for the initial implementation of the `e-Orbit` help center, especially for:

- home / hub
- first steps
- task pages
- troubleshooting
- downloads
- MVP Phase 1 visual support

It is designed so that content, design, or visual production teams can:
- prioritize images
- draft consistent prompts
- produce variations
- control visual style
- map each image to a specific page

---

## 2. General recommendations for AI image generation

### Recommended visual style
Use a style that is:
- clean
- technical
- realistic
- contemporary
- useful for documentation
- not overly promotional

### Avoid
- cluttered backgrounds
- futuristic renders
- unrealistic invented interfaces
- deformed hands
- generated text inside the image
- confusing iconography
- excessive glow or dramatic lighting

### Practical recommendation
When the image is product-focused:
- prefer neutral backgrounds or clean residential environments
- show the lock clearly
- use natural or controlled lighting
- use angles that help explain the product

When the image shows use:
- show a clear interaction
- one action per image
- simple composition
- focus on the point of use

When the image is app-related:
- ideally use a real screenshot
- if no screenshot exists, use a restrained mockup clearly meant as visual support

---

## 3. Suggested matrix fields
Each image should register:

- `id`
- `page`
- `image_type`
- `objective`
- `visual_description`
- `base_prompt`
- `negative_prompt`
- `format`
- `priority`
- `status`
- `notes`

---

## 4. Prioritized matrix for MVP Phase 1

### Image 1
**ID:** IMG-001  
**Page:** `/productos/e-orbit`  
**Suggested name:** Main product hero  
**Image type:** product / hero  
**Objective:** show e-Orbit as a smart lock installed and clearly visible  
**Visual description:** modern smart lock installed on an elegant residential door, clear view of the exterior panel, realistic environment, neutral background or contemporary interior  
**Base prompt:**  
Modern e-Orbit smart lock installed on a residential door, front view with slight angle, clean and elegant design, contemporary interior environment, soft natural lighting, clear focus on the product, simple composition for a help center, realistic product photography, tidy background, neutral tones, high definition  
**Negative prompt:**  
text inside the image, too many decorative objects, deformed hands, extreme perspective, exaggerated futuristic style, neon lights, plastic render, cluttered background, floating elements, fake interface  
**Format:** horizontal 16:9  
**Priority:** high  
**Status:** pending  
**Notes:** use as the main hub image

### Image 2
**ID:** IMG-002  
**Page:** `/productos/e-orbit/primeros-pasos`  
**Suggested name:** Product installed in real context  
**Image type:** usage / context  
**Objective:** show the product already installed and ready to use  
**Visual description:** door with e-Orbit installed in a clean residential setting, feeling of a product ready for setup  
**Base prompt:**  
Modern smart lock installed on a real apartment or house door, clean and realistic contextual view, tidy home environment, sense of product ready to be configured and used, documentary-style photography, balanced natural light, main focus on the lock and the door, clear composition for a technical guide, believable materials, high definition  
**Negative prompt:**  
clutter, overly decorative objects, darkness, dramatic advertising look, embedded text, distortions, futuristic style, artificial render, busy background  
**Format:** horizontal 4:3  
**Priority:** high  
**Status:** pending  
**Notes:** useful for first steps and installation content

### Image 3
**ID:** IMG-003  
**Page:** `/productos/e-orbit/usuarios/agregar-administrador`  
**Suggested name:** Interaction with panel to create administrator  
**Image type:** action / use  
**Objective:** visually support the initial user setup flow  
**Visual description:** adult hand interacting with the touch panel or keypad of the lock, clear focus on the panel area  
**Base prompt:**  
Realistic close-up of an adult person interacting with the panel or keypad of a modern smart lock installed on a door, clear focus on the setup action, natural and well-proportioned hand, clean composition, discreet background, technical and documentary style, soft lighting, realistic product and usage photography, high definition  
**Negative prompt:**  
deformed hands, extra fingers, tiny text as main element, invented complex interface, extreme angle, cluttered background, futuristic aesthetic, exaggerated reflections, low resolution  
**Format:** vertical 4:5  
**Priority:** high  
**Status:** pending  
**Notes:** if a real screenshot becomes available later, this can remain as secondary support

### Image 4
**ID:** IMG-004  
**Page:** `/productos/e-orbit/uso/pin`  
**Suggested name:** Using the keypad for PIN  
**Image type:** product detail  
**Objective:** clearly show use of the keypad or numeric input area  
**Visual description:** close-up of the lock keypad, finger approaching or pressing, very clear composition  
**Base prompt:**  
Detailed close-up of the keypad of a modern smart lock, an adult hand entering a PIN, sharp focus on the keypad surface, realistic product photography, soft lighting, minimal and technical composition, discreet blurred background, high definition  
**Negative prompt:**  
strange numbers, highly visible invented text, deformed hands, excessive reflections, exaggerated futuristic aesthetic, visual noise  
**Format:** vertical 4:5  
**Priority:** medium  
**Status:** pending  
**Notes:** avoid depending on correct visible numbers

### Image 5
**ID:** IMG-005  
**Page:** `/productos/e-orbit/uso/huella`  
**Suggested name:** Using the fingerprint reader  
**Image type:** product detail  
**Objective:** show how the finger rests on the sensor  
**Visual description:** finger naturally placed on the fingerprint reader of the lock  
**Base prompt:**  
Realistic close-up of a person using the fingerprint reader of a modern smart lock, finger resting naturally on the sensor, sharp focus on the contact point, clear and instructional composition, technical photography, soft lighting, neutral blurred background, high definition, restrained style for a help center  
**Negative prompt:**  
deformed fingers, extra hands, unclear sensor, robotic appearance, strange lighting, cluttered composition, text inside image, low resolution  
**Format:** vertical 4:5  
**Priority:** high  
**Status:** pending  
**Notes:** very important for support and troubleshooting

### Image 6
**ID:** IMG-006  
**Page:** `/productos/e-orbit/configuracion/idioma`  
**Suggested name:** Configuration or language change  
**Image type:** action / detail  
**Objective:** support the language change flow  
**Visual description:** active lock panel during configuration, hand interacting with the device  
**Base prompt:**  
Modern smart lock with active panel in configuration mode, adult hand interacting with the device, focus on the panel and the action, realistic photography, technical and clean style, simple tidy background, soft lighting, instructional composition for a help article, high definition  
**Negative prompt:**  
text-dominant panel, fantasy interface, deformed hands, cluttered background, extreme reflections, sci-fi style, low resolution, floating elements  
**Format:** vertical 4:5  
**Priority:** high  
**Status:** pending  
**Notes:** ideally later combine with a real screenshot or simple diagram

### Image 7
**ID:** IMG-007  
**Page:** `/productos/e-orbit/app/agregar-dispositivo`  
**Suggested name:** App use to add device  
**Image type:** app / usage context  
**Objective:** show the start of the flow from the phone  
**Visual description:** person holding a smartphone in front of the door with the lock, sense of initial pairing/setup  
**Base prompt:**  
Adult person holding a smartphone in front of a door with a modern smart lock, realistic scene of device configuration, clean home environment, clear balanced composition, shared focus between the phone and the lock, restrained documentary and technological photography, soft natural lighting, high definition  
**Negative prompt:**  
screen with highly visible fake text, deformed hands, strange perspective, messy background, exaggerated advertising aesthetic, fantasy interface, low resolution  
**Format:** horizontal 4:3  
**Priority:** high  
**Status:** pending  
**Notes:** if the real app is captured, this works as contextual imagery

### Image 8
**ID:** IMG-008  
**Page:** `/productos/e-orbit/app/vincular-por-qr`  
**Suggested name:** QR pairing  
**Image type:** action / app + product  
**Objective:** visually explain the interaction between phone and lock during the QR flow  
**Visual description:** smartphone showing a QR code in front of the lock, clear and tidy scene  
**Base prompt:**  
Realistic scene of pairing a smartphone and a smart lock using a QR code, phone displaying a generic QR code in front of the lock, clean and tidy indoor environment, instructional composition, clear technical photography, controlled lighting, high definition, restrained style for a help center  
**Negative prompt:**  
deformed QR, invented text as main element, extra hands, unrealistic screens, futuristic style, neon lights, cluttered background, low resolution  
**Format:** horizontal 4:3  
**Priority:** high  
**Status:** pending  
**Notes:** do not use as technical proof of the QR flow, only as conceptual support

### Image 9
**ID:** IMG-009  
**Page:** `/productos/e-orbit/solucion-de-problemas/no-reconoce-huella`  
**Suggested name:** Fingerprint reading problem  
**Image type:** troubleshooting / usage  
**Objective:** illustrate a recognition issue  
**Visual description:** user attempting fingerprint access with a neutral expression of doubt, focus on the reader  
**Base prompt:**  
Realistic scene of a person trying to use the fingerprint reader of a smart lock and encountering a small difficulty, subtle expression of doubt or review, focus on the reader and the interaction, clean environment, documentary photography, clear composition for a troubleshooting article, restrained tone, high definition  
**Negative prompt:**  
exaggerated drama, caricature-like expressions, deformed hands, busy background, ad-like aesthetic, embedded text, low resolution  
**Format:** vertical 4:5  
**Priority:** medium  
**Status:** pending  
**Notes:** keep the tone sober, not alarmist

### Image 10
**ID:** IMG-010  
**Page:** `/productos/e-orbit/solucion-de-problemas/no-conecta-a-la-app`  
**Suggested name:** App connection problem  
**Image type:** troubleshooting / app  
**Objective:** illustrate a connection issue between phone and lock  
**Visual description:** person with smartphone in front of the lock, sense of attempted connection without drama  
**Base prompt:**  
Realistic scene of a person trying to connect a smart lock with a mobile app, smartphone in hand in front of the door, slight gesture of review or waiting, clean home environment, clear and restrained composition for a troubleshooting article, realistic photography, high definition  
**Negative prompt:**  
huge fake error messages on screen, excessive drama, cluttered background, deformed hands, invented complex interface, futuristic aesthetic, low resolution  
**Format:** horizontal 4:3  
**Priority:** medium  
**Status:** pending  
**Notes:** if a real error screenshot is available later, keep this as secondary support

### Image 11
**ID:** IMG-011  
**Page:** downloads / documentation  
**Suggested name:** Product documentation  
**Image type:** editorial support  
**Objective:** support the manuals and downloads section  
**Visual description:** clean composition with product + printed docs or tablet showing a manual  
**Base prompt:**  
Realistic editorial composition with a modern smart lock next to documents or technical manuals on a clean desk, minimal style, restrained photography, professional and tidy environment, useful for a downloads or documentation section, neutral tones, high definition  
**Negative prompt:**  
messy papers, unreadable text as main focus, rigid corporate aesthetic, visual saturation, cluttered background, low resolution  
**Format:** horizontal 16:9  
**Priority:** low  
**Status:** pending  
**Notes:** optional for Phase 1, useful to enrich downloads

---

## 5. Master prompts by category

### A. Product hero
**Master prompt:**  
Modern smart lock installed on a residential door, realistic product photography, clean and contemporary environment, soft natural lighting, clear focus on the lock, tidy composition, neutral background, technical and elegant style for a help center, high definition

### B. Usage action
**Master prompt:**  
Adult person interacting with a modern smart lock installed on a residential door, realistic photography, single clear action, clean composition, soft lighting, tidy home environment, focus on the point of interaction, documentary style for a help center

### C. App + product
**Master prompt:**  
Person using a smartphone next to a modern smart lock, realistic setup or pairing scene, clean indoor environment, clear and instructional composition, balanced focus between phone and lock, restrained technical photography

### D. Troubleshooting
**Master prompt:**  
Realistic scene of smart lock usage with a small technical difficulty, subtle gesture of review or doubt, restrained composition, clean environment, clear focus on the interaction, documentary photography for a troubleshooting article

---

## 6. Master negative prompt
**Master negative prompt:**  
text inside the image, unreadable letters, fake complex interface, deformed hands, extra fingers, extreme perspective, cluttered background, exaggerated futuristic style, neon lights, plastic render, irrelevant objects, excessive drama, chaotic composition, low resolution

---

## 7. Quick format guide by use

### Main hero
- horizontal 16:9

### Article page
- horizontal 4:3 or vertical 4:5

### Cards / lists
- square 1:1 or vertical 4:5

### Download thumbnails
- horizontal 16:9

---

## 8. Real production priority to start implementation

### Produce first
- IMG-001 Main hero
- IMG-002 Installed product
- IMG-003 Add administrator action
- IMG-005 Fingerprint reader use
- IMG-006 Configuration / language
- IMG-007 Add device in app
- IMG-008 QR pairing

### Produce later
- IMG-004 PIN
- IMG-009 Fingerprint issue
- IMG-010 App connection issue
- IMG-011 Downloads

---

## 9. Operational recommendation
For real implementation, use this flow:

### Step 1
Generate **1 to 3 variants per priority image**

### Step 2
Choose one by:
- clarity
- realism
- documentary usefulness
- consistency with the product

### Step 3
Refine if needed by adjusting:
- angle
- background
- hand / interaction
- lighting
- framing

### Step 4
Name files consistently:
- `e-orbit-hero-main.jpg`
- `e-orbit-add-admin.jpg`
- `e-orbit-fingerprint-use.jpg`
- `e-orbit-app-add-device.jpg`

---

## 10. Final note
This document is the base for visual production with AI and can be used in parallel with implementation work.
