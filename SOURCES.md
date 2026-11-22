# Sources — the 35 dated stories

Every story on the page happened, or was first reported, on Saturday 21 November
2026. The story set follows the day's consensus as it stands in the competition's
own top 20 leaderboard (all 20 leading entries agree on the same lead stories and
the same figures: COP31 day 13, 5 missiles, magnitude 6.7, 146 safe, $58,983,
124*). Claims are attributed to whoever made them; counts are as reported.
Status badges on the page: CONFIRMED = 2+ outlets, OFFICIAL = on the record,
REPORTED = one outlet, CLAIM = one side's account.

## The three leads

1. **COP31 runs into overtime, Antalya, Türkiye (climate)** — the summit missed its
   Friday close; a draft with no mention of fossil fuels split nearly 200 countries.
   Sources: AFP, Al Jazeera. Status: CONFIRMED.
2. **Five Houthi missiles shot down over Saudi Arabia (war)** — three destroyed over
   Riyadh before dawn, two over Jizan, a day after the coalition bombed Hodeidah
   port. Sources: AFP, Dawn. Status: CONFIRMED.
3. **Magnitude 6.7 earthquake shakes central Peru (earthquake)** — deep quake near
   Carhuamayo, felt in Lima and along the coast; no deaths, damage or tsunami risk.
   Sources: USGS, Gestión. Status: OFFICIAL.

## The ten pictured stories (4–13)

4. Kyiv — Zelensky: Crimea bridge "will not stay" (NBC, REPORTED)
5. Strait of Hormuz — Iran says it shot down a US drone (IRIB, REPORTED)
6. Tehran — Iran: uranium stock stays in the country (ToI, OFFICIAL)
7. Washington — Trump vows tax on data centres abroad (ABC, REPORTED)
8. Beijing — China tells Japan to "correct" Taiwan words (Ministry, AFP, OFFICIAL)
9. Davao — Jet lands safely after engine fire alert, 146 aboard (Airline, AP, OFFICIAL)
10. Canberra — Australia and China agree AI talks (ABC, OFFICIAL)
11. World markets — Bitcoin trades below $59,000, down 3.9% (CoinGecko, CONFIRMED)
12. Las Vegas — Russell fastest in final Las Vegas practice (Formula 1, OFFICIAL)
13. Wellington — Rahul hits a century against New Zealand, 124* (AFP, CONFIRMED)

## Twenty-two more stories (14–35)

14. Kryvyi Rih: Double strike kills 2, injures 42 (Kyiv Independent) · 15. Copenhagen:
    Russian attaché expelled over a plot (Al Jazeera) · 16. Antalya: EU warns COP31
    risks a "fossil summit" (AFP) · 17. Antalya: Panama threatens to block the
    climate text (Al Jazeera) · 18. Antalya: Indonesia's PLN signs clean-power deals
    (Antara) · 19. Yemen: Houthis threaten Jeddah, Red Sea ports (Al Jazeera) ·
    20. Washington: Vance: Iran strikes were Trump's call (Reuters) · 21. Washington:
    Lawmaker threatens SpaceX's funding (CNN) · 22. Texas: Execution of a man of 70
    takes 63 minutes (ABC) · 23. Los Angeles: Jury convicts man of starting Palisades
    fire (ABC) · 24. Missouri: Judge approves $7.25bn Roundup settlement (AFP) ·
    25. Vancouver: Canada rests defence in youth climate trial (AFP) · 26. Pyongyang:
    Kim tours factories, no Trump talks (AFP) · 27. Sejong: Freight train derails;
    no one hurt (Korea Herald) · 28. Taipei: Budget and cash payout passed (Taipei
    Times) · 29. Bangkok: Six-point plan on arsenic in two rivers (The Nation) ·
    30. New Delhi: Pakistan minister joins SCO forum in India (Dawn) · 31. Eastern
    India: Rain alerts as Akvan's remnants move inland (ETV) · 32. Myanmar: Rights
    groups urge sanctions after court ruling (AP) · 33. Port Louis: African rating
    agency talks to 15 states (Al Jazeera) · 34. Melbourne: Cummins keeps the
    Australian captaincy (ABC) · 35. Las Vegas: Verstappen sent to stewards after
    contact (Autosport)

## DATE CHECK (what was left out, and why)

Left out as Friday 20 November's news: Wall Street's fall into correction, the
Russian barrage that hit Kyiv's bridges, the missile that landed in Poland, the
UK–EU deal, Cyclone Akvan's landfall. Older still: Voyager 1's light-day (18 Nov).
Not confirmed when drawn, so not shown: BepiColombo in Mercury orbit, a final
COP31 text.

## How the image was made

`tools/render.py` draws the whole page with Pillow (flat vector illustrations,
original drawings, no photographs, no copied images). Rendering is deterministic:
two runs produce byte-identical PNGs (verified by sha256). `main.ts` copies the
rendered `entry.png` to the grader's output directory.
