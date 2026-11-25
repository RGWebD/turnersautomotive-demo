# Turner's Automotive — single source of facts (see ../notes.md for sources)
NAME="Turner’s Automotive"; LEGAL="Turner’s Auto LLC"; SHORT="Turner’s Automotive"
REPO="turnersautomotive-demo"; BASE=f"https://rgwebd.github.io/{REPO}/"
STREET="135 Commercial Cir"; CITY="Keystone Heights"; REGION="FL"; ZIP="32656"
ADDR=f"{STREET}, {CITY}, {REGION} {ZIP}"
PHONE="(352) 473-3404"; TEL="tel:+13524733404"; SMS="sms:+13524733404"
LAT=29.7842377; LNG=-82.0258645
GPLACE="https://www.google.com/maps/place/TURNER%E2%80%99S+AUTOMOTIVE/@29.7842377,-82.0284394,17z/data=!3m1!4b1!4m6!3m5!1s0x88e60f70cee715e9:0x8879cd5ee60d667d!8m2!3d29.7842377!4d-82.0258645!16s%2Fg%2F1v75sqx7"
GLIST="https://maps.app.goo.gl/gTGMU6ZF7AFFTeKB7"
DIR="https://www.google.com/maps/dir/?api=1&destination=TURNER%E2%80%99S+AUTOMOTIVE%2C+135+Commercial+Cir%2C+Keystone+Heights%2C+FL+32656"
FB="https://www.facebook.com/people/Turner-Automotive-Transmission-AKA-The-Transmission-Repair-Shop/100063788893662/"
RATING=4.7; COUNT=247
HOURS_TXT="Mon–Fri 8 AM–5 PM"
# photos: alt text
PH={
'g01':"Turner’s Automotive shop in Keystone Heights: a lifted black pickup beside a blue two-post lift under the covered bays, with the Wheel Alignment banner",
'g04':"A dark blue Chevrolet Silverado parked in a covered service bay between lift posts",
'g05':"A Chevrolet Silverado raised on a lift with the hood open, oil drain cart below",
'g06':"A red Ford F-150 up on the four-post alignment rack beside the wheel alignment machine",
'g07':"A silver Mercedes-Benz on a two-post lift with the hood up",
'g08':"A black Shelby Mustang with the hood open in the shop",
'g09':"A silver Honda raised on a lift mid-repair, with drivetrain parts out on a jack stand",
'g10':"A Class C motorhome in the bay with the hood open for engine work",
'g11':"An older maroon Ford F-150 pickup waiting under the shop canopy",
'g12':"A silver Ford Escape inside the enclosed service bay next to lift posts and shop tools",
'g14':"A black GMC Acadia up on the alignment rack with the hood open",
'g15':"A white Ram dually pickup with a grille guard and the hood open for engine work",
'g16':"A lifted black Jeep Wrangler on off-road tires outside the shop bays",
'g17':"The Turner’s Automotive lot: the transmission shop building and the long covered service canopy",
'g19':"A white C5 Chevrolet Corvette in the lot, with a GMC SUV raised on the rack behind it",
'g20':"A red Mazda RX-7 with the hood up and the engine exposed",
'g21':"A black Honda Civic coupe with the hood up under the canopy",
'g22':"A white Chevrolet Silverado raised on the drive-on rack against a blue sky",
'g23':"A white Ford Mustang GT parked between the lift posts",
'g24':"A Jayco Class C motorhome up on the drive-on rack",
'g25':"A lifted black Chevrolet Silverado next to a blue two-post lift",
}
# services: from their site (keystone-auto-repair.com, Apr 2026 archive) plus jobs named in Google reviews
SERV=[
 dict(id="transmissions",t="Transmissions & drivetrain",ic="gear",img="g09",g="1",
      s="Automatic and manual transmissions, differentials and gearboxes.",
      d="Transmission work is where this shop started: their site is titled “Turner’s Automotive & Transmission,” their Facebook page calls it “The Transmission Repair Shop,” and the sign on the building still reads The Transmission Shop. Their site lists transmissions, differentials and gearboxes.",
      li=["Transmissions (from their site)","Differentials and gearboxes (from their site)","Transmission repair is a top topic in Google reviews"]),
 dict(id="diagnostics",t="Diagnostics & check engine light",ic="diag",img="g15",g="2",
      s="Check engine and service engine soon lights, tracked down to the real cause.",
      d="“Problem diagnosis” is the most-mentioned topic in their Google reviews. One customer’s problem was “diagnosed in less than 15 minutes.” Another thought he had a blown head, and it turned out to be a loose spark plug wire.",
      li=["Check engine and service engine soon lights (from their site)","Problem diagnosis: 13 Google review mentions","The mechanic shows you the broken part"]),
 dict(id="brakes-suspension",t="Brakes, shocks & struts",ic="brake",img="g07",g="3",
      s="Brakes, rotors, shocks, struts, steering and suspension.",
      d="Their site lists brakes, shocks and struts. Reviewers also mention calipers, rotors, and steering and suspension work. One customer came in for a full brake job and was told he only needed one caliper and his rotors turned.",
      li=["Brakes, shocks and struts (from their site)","Calipers and rotors (Google reviews)","Steering and suspension (Google reviews)"]),
 dict(id="ac-cooling",t="A/C, heating & cooling",ic="cool",img="g20",g="4",
      s="A/C and heat, radiators, coolant, water pumps and timing belts.",
      d="Their site lists A/C and heating repair and radiator and coolant system repair. The shop’s own Google post shows a timing belt, tensioner and water pump replaced on a 2005 PT Cruiser, along with a new radiator cap.",
      li=["A/C and heating system repair (from their site)","Radiator and coolant system repair (from their site)","Timing belt and water pump jobs (shop’s Google post)"]),
 dict(id="engine-fuel",t="Engine & fuel systems",ic="fuel",img="g08",g="5",
      s="Engine repair, carburetors, fuel injection and fuel pumps.",
      d="Their site lists carburetor, fuel injection and fuel pump repair, and reviewers describe engine repairs on everything from daily drivers to work trucks.",
      li=["Carburetor and fuel injection repair (from their site)","Fuel pump repair (from their site)","Engine repair (Google reviews)"]),
 dict(id="electrical",t="Electrical: battery, starter & alternator",ic="batt",img="g12",g="6",
      s="Batteries, starters, alternators, generators and wiring.",
      d="Their site lists electrical repair, including batteries, starters, alternators and generators. One reviewer describes a mechanic who took “a few extra minutes to replace a wire” after finding a melted part.",
      li=["Battery, starter, alternator and generator (from their site)","Wiring repairs (Google reviews)"]),
 dict(id="maintenance",t="Oil change, tune-up & fluids",ic="oil",img="g05",g="R",
      s="Oil change, lube and tune-up, filters, fluids, belts and hoses.",
      d="Oil change is listed on their Google profile. Their site adds lube and tune-up, plus filters, fluids, belts and hoses. One customer called in, was told to “bring it in anytime,” and had a synthetic oil change done while she had lunch nearby.",
      li=["Oil change, lube and tune-up (from their site)","Filters, fluids, belts and hoses (from their site)","Oil change (Google profile)"]),
 dict(id="alignment",t="Wheel alignment & tires",ic="align",img="g06",g="N",
      s="Wheel alignments on the drive-on rack, plus tire work.",
      d="Their site lists alignments, and the big Wheel Alignment banner hangs on the canopy. Reviewers also mention tire work, including small trailer tires.",
      li=["Alignments (from their site)","Tire work, including trailer tires (Google reviews)"]),
]
MODELS=["Domestic cars & trucks","Import cars & trucks","Vans","4×4","Special interest vehicles"]
# reviews, word for word (Google Maps, Nov 25 2026). name, meta, text
REV=[
 ("Joy Davis","Local Guide · 2 months ago","In a world full of uncertainty, as a busy female, it was really nice to go to Turner's. I experienced the problem being diagnosed in less than 15 minutes, parts ordered, replaced, and out the door all in a few hours. Everyone was pleasant and the mechanic took the time to show me the broken part and to specifically point out where & how it had \"melted\", also being concerned that he had taken a few extra minutes to replace a wire. (going above & beyond). For me, I was extremely happy and confident when leaving. It was so much better than previous experiences in other locations. Yes. all of these things make a difference. Thank you Turner's💯💯💯."),
 ("Yordanos Afework","6 months ago","Turner’s Automotive is truly an amazing company! From start to finish, the experience was nothing short of excellent. The team is professional, honest, and genuinely cares about their customers. I especially want to highlight Mrs. Debra—she is absolutely wonderful. She was so helpful, patient, and supportive throughout the entire process. She took the time to answer all my questions, made me feel comfortable, and went above and beyond to ensure everything was handled smoothly. It’s rare to come across a place that combines great service with such kindness and integrity. I highly recommend Turner’s Automotive to anyone looking for trustworthy and compassionate service. I will definitely be returning!"),
 ("YuMad Bro?","a month ago","Still amazed by the exceptional level of service this mechanic gives to my vehicles. Thought I had a blown head, turns out one of my spark plug wires was loose. They could have got me for thousands but we're honest. That's a rare quality for a mechanic. They got my business for life!"),
 ("Adam Batchelor","Local Guide · a year ago","9/25/25: I thought I was in need of full brake job front and back all around, plus rotors and an A/C charge. This was what I asked them to complete. They could have charged me for all this work and I would have been none the wiser. Instead they advised me I only needed 1 brake caliper, rotors turned and a new A/C cabin air filter. I have never met or dealt with ANY automotive repair shop that was as fair and honest as these people. If they tell you something is wrong.... it is. If they tell you that you got time left on parts or there is nothing wrong and you're wasting money you can take it to the bank. They have all my future business, and I highly recommend their services to anyone in Keystone Heights or just passing through. You will NOT get ripped off here!"),
 ("Steven Skinner","Local Guide · 2 years ago","Truly my new auto service shop! This was the second vehicle they worked on for me. They'll quote you the work and the price doesn't change unless an unforeseen issue arises. You'll get a call from Doug with the update and whether you want them to proceed with the fix. They have a night drop slot so you can drop off your car after hours and have a ride home. You fill out an envelope with your information and the issue with the car, put the key in the envelope, and drop it in the slot. The next day or two, you'll get a call from Doug letting you know your vehicle is ready. Joey's Team is spot on...great work, quick turnaround, and great prices!! Turner's Automotive and Transmission was $800 cheaper then what the dealership quoted me. And yes... Both vehicles are running and driving great!!"),
 ("Stephanie Roop","a year ago","We've taken our van there a couple of times and they are just fantastic. They kept us informed on what the problem was and what they were doing. They didn't pressure us into any extra work, even if they recommend something. And their prices are very fair. Such a great experience!"),
 ("Deanna shea","Local Guide · a year ago","I needed an oil change. This was the 2nd place I called yesterday. The 1st said they were too busy. The nice ladies in the office told me to bring it in anytime. I got there at 11am. While doing paperwork and chatting my car was started and I walked next door to shop and then had lunch at the Irish pub. My car was ready quick. A fully synthetic oil change and all my fluids were topped off was $70 a very fair price. I recommend this place and will be back next oil change and will bring my truck here as well."),
 ("Kevin Takach","a year ago","5 stars are not enough to say about Joey and his team, For over a decade I have taken my vehicles to his shop and have never been more impressed with the outcome, Honest, Quality, and trustworthy work is hard to find these days and this business is a trifecta when you choose them."),
 ("Ashley Nicole","Local Guide · 5 months ago","I am new to the area and needed my car fixed a couple times. The techs are fantastic and Mrs. Turner in the office is one of the nicest people I've met since moving to KSH. Their service is fast and reliable. Also had the pleasure of speaking to Mr. Turner himself and he is also very kind."),
 ("Paul Davis","a year ago","These guys are great, we were camping at the state park when the check engine light came on. They found the problem, got the part on time did the work at a good price; plus they helped getting me to and from my camp site. If i lived up there I most certainly would become a regular."),
]
FAQ=[
 ("What are Turner’s Automotive’s hours?","Monday through Friday, 8 AM to 5 PM Eastern Time. Closed Saturday and Sunday. Google flags Thanksgiving (Nov 26) and the day after (Nov 27) as “hours might differ,” so call ahead on holidays."),
 ("Where is the shop?",f"{ADDR}, on Commercial Circle in Keystone Heights, Florida. Their site says they serve Keystone Heights and the wider Northeast and Central Florida area."),
 ("Do you work on transmissions?","Yes. Transmissions, differentials and gearboxes are the first services on their site, which is titled “Turner’s Automotive & Transmission.”"),
 ("What vehicles do you work on?","Their site lists domestic and import cars and trucks, vans, 4×4s and special interest vehicles. The shop’s photos also show motorhomes, lifted trucks and classic sports cars."),
 ("Can I drop my car off after hours?","Reviewers describe a night drop slot: fill out an envelope with your details and the problem, put the key inside and drop it in the slot. Call the shop to confirm before you rely on it."),
 ("How do I get an estimate?",f"Call {PHONE} during business hours, or use the estimate form on this page. It opens a pre-filled text message to the shop’s number (please confirm the number accepts texts)."),
 ("What payment do you take?","Their Google profile lists credit and debit cards. Ask about payment options when you call."),
]
