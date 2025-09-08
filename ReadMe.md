# This is a tracker and statistics calculator for the TV show "Are you the one?"

## Rules  of the show

The show is **highly trashy** and I wouldn't 
recommend it to anyone who likes intellectual 
conversations. But it gets interesting when 
looking from a mathematical perspective!

### Setting

10 persons from one hetero normative gender 
and 11 from the other are placed into a villa 
and have a predefined "perfect match" which 
they have to find. (one triple match included)

They only win the show - and the prize money - 
if everyone finds their match.

Using math we can now find out how many 
different possible solutions exist:

11! possible placements for the members 
of the bigger group to be positioned.
And 10 different positions where the eleventh 
can take place to create a triple pairing.

11! * 10 = 399.168.000 different solutions.

... But matches can only be identified by two methods:

### Matchbox (max 10)

The candidates vote one pair to go in the "Matchbox". 
Then they get a straight answer afterward: **Match** 
or **No Match**.

### Matching night

The candidates group themselves into 10 pairs leaving 
one person alone. After that *n* lights turn on. The *n* 
signals how many perfect matches there are in the 10 pairs.

If they don't have 10 lights being turned on in the 10th night 
they lose the show.

## How to set up (for people that have never used GitHub, python or anything related to coding)

Since this project only exists because my friend 
wanted to know the outcome of her favourite show 
before other people I assume there are more people 
like her - who don't know a bit about code - 
I made this detailed step-by-step guide.

### Downloads

git, python, etc.

### Get Repository

## How to use

If everything is correctly set up you are ready to start. 
Just watch the show and when new information arrives - 
A *Matchbox* decision or a *Matching Night* - type it 
in the Excel sheet [AYTO Infos](AYTO_Infos.xlsx) and save the file.
Then run the [python script](main.py).

### Excel file explanations

In cells A1:A2 you can swap the labels depending on which group 
contains 11 or 10 candidates. In B1:L2 you write down a list 
of all candidates.

For everything else please note that the members of the 10-group 
are always written down on the left side. 

A6:B15 contains all positive *Matchbox* decisions. (Matches)

E6:F15 contains all negative *Matchbox* decisions. (No Matches)

H4:I15 contains data for night Nr. 1. You write alle the 
pairings in the cells H6:I15. In the cell I5 you write down the 
number of lights that turned on.

### Run the script

### Results of the script explained

### How the script works