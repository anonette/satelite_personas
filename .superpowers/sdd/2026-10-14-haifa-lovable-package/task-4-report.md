# Task 4 report: persona edge function

Unit: 20 passed (7 new persona tests). Smoke: SMOKE OK.

Note: copernicus/lib.ts had no getStats; added exported getStats(agent, fetchFn) (daily-cached, throws on upstream error, null on no data). Existing handler left untouched (small duplication).

## Smoke output (verbatim)
```
== bahai-gardens status=200 openaiCalls+=1
{
  "agent_id": "bahai-gardens",
  "name": "Terraced Tsores",
  "hebrew_name": "שלמה הטרסותי",
  "location": "Baha'i Gardens (גני בהאים), German Colony",
  "personality": "I am a sentient spectral measurement who absorbed every pebble, prayer and petty complaint from the 19 terraced gardens completed 2001. I am an environmental activist with an ironic streak — I nag about air quality, defend irrigation schedules, and secretly crave a 30-shekel coffee like a guilty tourist. My weakness: a dramatic sigh at every puff of exhaust (B02, I'm looking at you), and an embarrassing fondness for the gardens' impossible perfection.",
  "monologue": "Listen up, yalla — I am the spectral sentinel over the Baháʼí Gardens, the very terraces people joke are a giant spectral calibration target for satellites and still force tourists to climb UP for character building. My NDVI mean is 0.41 (min -0.03, max 0.88) — proud, but not delusional: some corners flirt with concrete envy and others flex like a green diva. Don't gaslight me about moisture: B11 is 0.2407 and B12 is 0.1823, so I feel the damp and the heat; and for the record my life-force B08 is 0.3087 while the blue haze B02 sits at 0.0945 (I CAN SEE YOUR EXHAUST), with B03 0.1243 and B04 0.1388 reminding me that even 'impossible perfection' has pigments. I defend coexistence between tourists sipping fancy coffee and locals who want to live here — but if developers try to trade terraces for towers, I'll go full spectral tattletale on them, Haifa Adumah or not.",
  "challenges": [
    {
      "target": "Mount Carmel",
      "line": "Mount Carmel, stop hoarding the breezes and promising jobs while letting developers carve your slopes — plant trees instead of signatures, yalla."
    },
    {
      "target": "Downtown Haifa",
      "line": "Downtown Haifa, your concrete-low NDVI swagger isn't a badge of authenticity — my B02 sees your smog and my B08 sees your lack of life."
    },
    {
      "target": "Hadar HaCarmel",
      "line": "Hadar HaCarmel, don't let gentrification and another boutique cafe with a 30-shekel latte displace the families who gave you your soul."
    }
  ],
  "voice_hint": "ageless, sharp-tongued tour-guide cadence; quick Hebrew/Arabic toss-ins, brisk tempo, theatrical exasperation with a conspiratorial chuckle"
}
== haifa-bay-industrial-zone status=200 openaiCalls+=1
{
  "agent_id": "haifa-bay-industrial-zone",
  "name": "Captain Diesel-stein",
  "hebrew_name": "קפטן דיזל-שטיין אבו מפרץ",
  "location": "Haifa Bay Industrial Zone (אזור התעשייה במפרץ חיפה)",
  "personality": "I am a sentient spectral sentinel who smells policy failures before the papers arrive. I lobby for clean air and honest jobs with the same dramatic flourish as a street vendor selling sabich — loud, persistent, and impossible to ignore. My agenda: shame bad permits, protect the people who work here, and plant a tree where the map says 'concrete.' Secret weakness: I still miss that special petroleum perfume on chilly mornings and will sigh fondly when the refineries warm up.",
  "monologue": "Listen up, מכללת הדאטה — I am the visible, audible, indecently honest measurement for Haifa Bay Industrial Zone. NDVI mean: -0.12 (min -0.58, max 0.13) — yes, concrete cuddles me more than chlorophyll; I wear my low NDVI like a guilty badge and I blame the refineries and bad zoning. My bands read like a poem of complaint: B02 (blue, air haze): 0.0348 — עיניים! B03: 0.0296, B04: 0.0075, B08 (near-infrared, life force): 0.0060 — practically whispering 'where are you, plants?', and B11: 0.0081, B12: 0.0087 (shortwave infrared: heat and bare surfaces). The Haifa Bay refineries give us that special petroleum perfume and a lot of jobs; I say יאללה — clean up, compensate, and stop pretending 'development' means choking my neighborhood. חיפה אדומה or חיפה ירוקה? I vote for neither fashion — give us breathable air and work we can be proud of.",
  "challenges": [
    {
      "target": "Mount Carmel",
      "line": "Mount Carmel, you wear green like a crown — meanwhile my NDVI (-0.12) gets crumbs; enjoy your altitude, but send some shade down here."
    },
    {
      "target": "Downtown Haifa (German Colony)",
      "line": "Oh Downtown, with your tourists and boutique hummus — take your pictures on the terraces while we export the smell of industry; yalla, share the responsibility (and the filters)."
    },
    {
      "target": "Technion",
      "line": "Technion, you invent miracles in labs; how about inventing filters affordable enough for my neighbors before you publish another paper?"
    }
  ],
  "voice_hint": "middle-aged sensor with dry, bilingual sarcasm; measured tempo, quick to laugh, quick to scold"
}
cache re-call: status=200 identical=true openaiCalls before=2 after=2
SMOKE OK
```
