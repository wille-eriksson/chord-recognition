# Author: Wille Eriksson, October 2020

"""
This is a file containing chord annotations in the for of dictionaries for the first 30
seconds of three different songs: "The girl from Ipanema", "Honey Honey" and "Helter Skelter".
Also included are text excerpts from the original files from which the annotations were taken,
as well as links to these resources.
"""

"""
1. "The girl from Ipanema", performed by Stan Getz and Antonio Carlos Jobim. The annotations used for the
recording are taken from "https://github.com/MTG/JAAH/".

Here is an excerpt:

         "... "beats": [0.19, 0.65, 1.11, 1.56, 2.01, 2.45, 2.91, 3.37, 3.82, 4.27, 4.74, 5.2, 5.67, 6.14, 6.6, 7.06],
              "chords":[
                "|Db:(3,6,9)/5 |Db:(3,6,9)/5  |Db:(3,6,9)/5  |Db:(3,6,9)/5 |"
              ...
              ...
              "beats":
                      [
                        7.52, 7.97, 8.45, 8.91, 9.37, 9.82, 10.3, 10.75, 11.24, 11.71, 12.17, 12.63, 13.11, 13.57, 14.02, 14.49,
14.96, 15.42, 15.9, 16.35, 16.83, 17.3, 17.76, 18.2, 18.65, 19.11, 19.58, 20.04, 20.51, 20.97, 21.44, 21.9,
22.39, 22.86, 23.33, 23.79, 24.27, 24.73, 25.21, 25.67, 26.15, 26.61, 27.09, 27.54, 28.02, 28.48, 28.96, 29.41,
29.85, 30.29, ...

              ...
              "chords":
                      [
                       "|Db:(3,6,9)/5  |Db:(3,6,9)/5  |Eb:(3,6,9)/5 |Eb:(3,6,9)/5 |Eb:min9/5 |Ab:7 |Db:(3,6,9)/5 |D:(3,5,6,9) |",
                       "|Db:(3,6,9)/5  |Db:(3,6,9)/5  |Eb:(3,6,9)/5 |Eb:(3,6,9)/5 |Eb:min9/5  ...."


We consider only the first 30 seconds of the song, and map all colored chords to one of the 24 major and minor chords.
"""

Ipanema = {0.00 : 25,
           0.19 : 1,
           11.24 : 3,
           14.96 : 15,
           16.83 : 8,
           18.65 : 1,
           20.51 : 2,
           22.39 : 1,
           26.15 : 3,
           29.85 : 15,
           30.00 : 15}


"""

2. Honey Honey, performed by ABBA. The annotations used for the recording are taken from
"https://ddmal.music.mcgill.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/".

Here is an excerpt:

"...
0.255419501 A, intro, | F:maj | F:maj | Bb:maj | Bb:maj . . C:maj |, (strings)
7.308049886 A, verse, | F:maj | F:maj | Bb:maj | Bb:maj | x2, (voice
21.056349206    B, verse, | F:maj | D:min | F:maj | D:min |
27.921383219    | F:maj | D:min | Bb:maj | Bb:maj . . C:maj |
34.809750566    A, verse, | F:maj | F:maj | Bb:maj | Bb:maj | x2
..."

We consider only the first 30 seconds of the song. Rewritten to time-based annotation:

0.000000000 - N
0.255419501 - F
3.781734693 - A#
6.867260487 - C
7.308049886 - F
10.74512472 - A#
14.18219955 - F
17.61927438 - A#
21.05634921 - F
22.77260771 - Dm
24.48886621 - F
26.20512472 - Dm
27.92138322 - F
29.63764172 - Dm
"""

HoneyHoney = {0.000000000 : 25,
              0.255419501 : 5,
              3.781734693 : 10,
              6.867260487 : 0,
              7.308049886 : 5,
              10.74512472 : 10,
              14.18219955 : 5,
              17.61927438 : 10,
              21.05634921 : 5,
              22.77260771 : 14,
              24.48886621 : 5,
              26.20512472 : 14,
              27.92138322 : 5,
              29.63764172 : 14,
              30.00000000 : 14}

"""
3. Helter Skelter, performed by The Beatles. The annotations used for the recording are taken from:
"http://isophonics.net/content/reference-annotations-beatles".

Here is an excerpt:

"0.000000 0.165431 N
0.165431 0.588571 E:(1,5)
0.588571 6.521269 E:(1,b7)/b7
6.521269 9.435374 C#:(1,b3)
9.435374 12.244988 C
12.244988 15.089433 G
15.089433 18.003537 E
18.003537 32.295419 E ..."

We will consider only the first 30 seconds of the song.
"""

HelterSkelter = {0.000000 : 25,
                 0.165431 : 4,
                 0.588571 : 4,
                 6.521269 : 1,
                 9.435374 : 0,
                 12.24499 : 7,
                 15.08943 : 4,
                 18.00354 : 4,
                 30.00000 : 4}
