# This is a chunk of code to calculate Free E2 and Free T
# You are free to use it for whatever you want, just don't claim copyright over it.
#
# All quantities are normalised into mol/L as the various constants are in L/mol
#
# The equations used come from here: https://cebp.aacrjournals.org/content/11/10/1065
# They are from the 1st set by Vermeulen et al
#
# Following the reference to the linked paper, and extrapolating I also tried to calculate the Albumen bound E2
# Apparently around 60% of E2 is bound to Albumin and that's about the result I get so ...
#

E2 = input("E2 (pmol/L): ")
E2 = E2 * 1e-12

CSHBG = input("SHBG (nmol/L):")
CSHBG = CSHBG * 1e-9

fE2 = E2/100  # First cut estimate. The algorithm will refine this up or down until the require accuracy is reached.

T = input("T (nmol/L): ")
T = T * 1e-9


KaE2 = 4.21e4  # L/mol  - Affinity constant for E2 to bind to Albumin
Ca = 6.5e-4    # mol/L  - Apparently Albumen is normally in this concentration in the blood (from the paper above)
               #          Looking back at my labs it is spot on for one test and off 2% for another. I figure close enough
               # Vermeulen paper has this constant slightly lower at 6.2e-4

N2 = (KaE2 * Ca) + 1   # N2 from the equation in the reference. Albumen loves E2 even more than T
KsE2 = 3.14e8   # L/mol - Affinity constant for E2 to bind to SHBG
KaT = 4.06e4    # L/mol - Affinity constant to bind T to Albumin  - lower than E2?
KsT = 1.0e9     # L/mol - Affinity constant to bind  T to SHBG. It's a little over 3 x KsE2, but I thought I heard people say it was more
N1 = (KaT * Ca) + 1  # N1 calculation from the paper

fE2diff = 1    # can be any number to start off, gets refined each loop.

# My maths is too rusty to solve the equation properly, so I'm brute forcing it, trying values until I am
# within .01pmol/L of the answer. I figure that is accurate enough.

if False:
    while fE2diff > 1e-14:

        # The equation from the referenced paper for calculating fE2
        # I start with a guessed value first and run the calculation.
        #
        fE2p = (E2 - N2 * fE2)/(KsE2 * (CSHBG - E2 + (N2*fE2)))

        # See how close provisional and calculated values are
        fE2diff = abs(fE2p - fE2)

        # Neither of the values will be right,the right value will be somewhere in the middle.
        # We iterate until we get something close enough

        fE2 = (fE2 + fE2p)/2

else:

    increment = 1e-12 # We start at 1% and step upwards at first trying to find a closer answer
    fE2 = E2/100

    while fE2diff > 1e-15:

        # The equation from the referenced paper for calculating fE2
        # I start with a guessed value first and run the calculation.
        #
        fE2p = (E2 - N2 * fE2)/(KsE2 * (CSHBG - E2 + (N2*fE2)))

        # See how close provisional and calculated values are
        lastdiff = fE2diff   # how close were we last time
        fE2diff = abs(fE2p - fE2)  # calculate how close we were this time

        # If we are further away than last time, start moving in the other direction, but more slowly.
        if fE2diff > lastdiff:
            increment = -increment / 10

        # Neither of the values will be right,the right value will be somewhere in the middle.
        # We iterate until we get something close enough

        # print fE2*1e12, fE2p*1e12, fE2diff*1e12
        # raw_input("Iter: ")

        fE2 += increment # move to a closer value
        # fE2 = (fE2 + fE2p)/2


# We have iterated to within .01 of a pmol/L so that is the answer we print out
print "Free E2 pmol/L = {0:.2f}".format(fE2 * 1.0e12)
print "Free E2 % = {0:.2f}".format(fE2/E2*100)


# Not confident of this equation, but it is the E2 equivalent of the T equation in the Vermuelen paper
AE2 = KaE2*Ca*fE2
print "Albumin bound E2 = {0:.2f}".format(AE2 * 1.0e12)

# Same algorithm again, but this time for T

fTdiff = 1
fT = T/100
increment = 1.0e-9
while fTdiff > 1e-15:
    fTp = (T - N1 * fT)/(KsT * (CSHBG - T + (N1*fT)))
    lastdiff = fTdiff
    fTdiff = abs(fTp - fT)
    if fTdiff > lastdiff:
        increment = -increment / 10
    fT += increment

print "Free T (pmol/L) = {0:.2f}".format(fT * 1.0e12)
print "Free T % = {0:.2f}".format(fT/T*100)
AT = KaT*Ca*fT
print "Albumin bound T (nmol/L) = {0:.2f}".format(AT * 1.0e9)
SHBGT = (T-AT-fT)
print "SHBG bound T (nmol/L) = {0:.2f}".format(SHBGT*1e9)

if SHBGT > CSHBG / 20:
    print "T is stealing a lot of SHBG, so Free E value is probably a bit lower than it should be"

E2 = raw_input(" Press Enter to Finish: ")

exit()