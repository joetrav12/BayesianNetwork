import random
from numpy import *

# PART A)
print("PART A)")

# going to be using this method for all parts of the problem:
def compute_probability(sky_var, sprinkler_var, rain_var, grass_var):
    sky_p = .5 # P(sky=sunny) = P(sky=cloudy) = 5, so we can just intialize sky_p to .5
    # initializing the rest of the probabilities:
    sprinkler_p = 0
    rain_p = 0
    grass_p = 0

    # the following conditionals are derived from the Bayesian network provided:
    if sky_var == "cloudy":
        if sprinkler_var == "on":
            sprinkler_p = .5
        elif sprinkler_var == "off":
            sprinkler_p = 1 - .5
        else:
            raise "ERROR: UNDEFINED VARIABLE"
        if rain_var == "yes":
            rain_p = .7
        elif rain_var == "no":
            rain_p = 1 - .7
        else:
            raise "ERROR: UNDEFINED VARIABLE"
    elif sky_var == "sunny":
        if sprinkler_var == "on":
            sprinkler_p = .9
        elif sprinkler_var == "off":
            sprinkler_p = 1 - .9
        else:
            raise "ERROR: UNDEFINED VARIABLE"
        if rain_var == "yes":
            rain_p = .01
        elif rain_var == "no":
            rain_p = 1 - .01
        else:
            raise "ERROR: UNDEFINED VARIABLE"
    else:
        raise "ERROR: UNDEFINED VARIABLE"

    if sprinkler_var == "on" and rain_var == "yes":
        if grass_var == "dry":
            grass_p = 1 - .99
        elif grass_var == "wet":
            grass_p = .99
        else:
            raise "ERROR: UNDEFINED VARIABLE"
    # combining these two conditionals because they have the same result:
    elif (sprinkler_var == "on" and rain_var == "no") or (sprinkler_var == "off" and rain_var == "yes"):
        if grass_var == "dry":
            grass_p = 1 - .9
        elif grass_var == "wet":
            grass_p = .9
        else:
            raise "ERROR: UNDEFINED VARIABLE"
    elif sprinkler_var == "off" and rain_var == "no":
        if grass_var == "dry":
            grass_p = 1 - .01
        elif grass_var == "wet":
            grass_p = .01
        else:
            raise "ERROR: UNDEFINED VARIABLE"
    else:
        raise "ERROR: UNDEFINED VARIABLE"

    return sky_p * sprinkler_p * rain_p * grass_p

# the domains of the variables:
sky = ["cloudy", "sunny"]
sprinkler = ["on", "off"]
rain = ["yes", "no"]
grass = ["dry", "wet"]
# array for the 2^4 probabilities:
probabilities = []

# the following intializations are for PART B):
grass_dry_probabilities = []
grass_wet_probabilities = []

for i in sky:
    for j in sprinkler:
        for k in rain:
            for l in grass:
                p = compute_probability(i, j, k, l)
                p_sig = '%s' % float('%.5g' % p) # reduce significant digits
                print("P(sky=" + i + ", sprinkler=" + j + ", rain=" + k + ", grass=" + l + ") =", p_sig)
                probabilities.append(p)
                # the following code is for PART B):
                if l == "dry":
                    grass_dry_probabilities.append(p)
                if l == "wet":
                    grass_wet_probabilities.append(p)

print("sum of probabilities:", sum(probabilities))
print("\n")


# PART B)
print("PART B)")

P_grass_dry = sum(grass_dry_probabilities)
P_grass_wet = sum(grass_wet_probabilities)
# these are to confirm that each table sums to 1:
##grass_dry_sum = 0
##grass_wet_sum = 0
grass_dry_probabilities = []
grass_wet_probabilities = []

# for dry grass:
for i in sky:
    for j in sprinkler:
        for k in rain:
            p = compute_probability(i, j, k, "dry") / P_grass_dry
            # not doing significant digits here because decimal values are not as nice as in PART A):
            print("P(sky=" + i + ", sprinkler=" + j + ", rain=" + k , "| grass=dry) =", p)
            #grass_dry_sum = grass_dry_sum + p
            grass_dry_probabilities.append(p)

# the way python adds it comes out to .999999, so rounding to exactly 1:
print("sum of probabilities =", '%s' % float('%.5g' % sum(grass_dry_probabilities)))
print();

# for wet grass:
for i in sky:
    for j in sprinkler:
        for k in rain:
            p = compute_probability(i, j, k, "wet") / P_grass_wet
            print("P(sky=" + i + ", sprinkler=" + j + ", rain=" + k , "| grass=wet) =", p)
            #grass_wet_sum = grass_wet_sum + p
            grass_wet_probabilities.append(p)

print("sum of probabilities =", sum(grass_dry_probabilities))
print("\n")


# PART C)
print("PART C)")
samples = 1000

# for dry grass:
dry_sky_samples = []
dry_sprinkler_samples = []
dry_rain_samples = []

# sample 0 (picked randomly):
dry_sky_samples.append("cloudy")
dry_sprinkler_samples.append("on")
dry_rain_samples.append("yes")

for i in range(1, samples):
    # need to derive the probability from the previous samples
    # grass is always dry for this sampling
    sky_sample_p = compute_probability("cloudy", dry_sprinkler_samples[i-1], dry_rain_samples[i-1], "dry") / (compute_probability("sunny", dry_sprinkler_samples[i-1], dry_rain_samples[i-1], "dry") + compute_probability("cloudy", dry_sprinkler_samples[i-1], dry_rain_samples[i-1], "dry"))
    sprinkler_sample_p = compute_probability(dry_sky_samples[i-1], "on", dry_rain_samples[i-1], "dry") / (compute_probability(dry_sky_samples[i-1], "off", dry_rain_samples[i-1], "dry") + compute_probability(dry_sky_samples[i-1], "on", dry_rain_samples[i-1], "dry"))
    rain_sample_p = compute_probability(dry_sky_samples[i-1], dry_sprinkler_samples[i-1], "yes", "dry") / (compute_probability(dry_sky_samples[i-1], dry_sprinkler_samples[i-1], "no", "dry") + compute_probability(dry_sky_samples[i-1], dry_sprinkler_samples[i-1], "yes", "dry"))

    # picking a random number; if rand <= p, add the corresponding condition to the samples array
    rand = random.uniform(0, 1)
    if rand <= sky_sample_p:
        dry_sky_samples.append("cloudy")
    else:
        dry_sky_samples.append("sunny")
        
    rand = random.uniform(0, 1)
    if rand <= sprinkler_sample_p:
        dry_sprinkler_samples.append("on")
    else:
        dry_sprinkler_samples.append("off")
        
    rand = random.uniform(0, 1)
    if rand <= rain_sample_p:
        dry_rain_samples.append("yes")
    else:
        dry_rain_samples.append("no")    

sum_ = 0
index = 0
for i in sky:
    for j in sprinkler:
        for k in rain:
            count = 0
            for l in range(samples):
                # this finds each instance of a scenario and counts it:
                if dry_sky_samples[l] == i and dry_sprinkler_samples[l] == j and dry_rain_samples[l] == k:
                    count = count + 1
            percent_error = 100*abs(count/samples - grass_dry_probabilities[index])
            pe_sig = '%s' % float('%.2g' % percent_error)
            # displays the percent of samples that were the given scenario:
            print("gibbs_estimated_probability(sky=" + i + ", sprinkler=" + j + ", rain=" + k , "| grass=dry) =", count/samples, "-> percent error =", pe_sig)
            index = index + 1
            sum_ = sum_ + count/samples

print()

# for wet grass:
wet_sky_samples = []
wet_sprinkler_samples = []
wet_rain_samples = []
wet_sky_samples.append("cloudy")
wet_sprinkler_samples.append("on")
wet_rain_samples.append("yes")

for i in range(1, samples):
    sky_sample_p = compute_probability("cloudy", wet_sprinkler_samples[i-1], wet_rain_samples[i-1], "wet") / (compute_probability("sunny", wet_sprinkler_samples[i-1], wet_rain_samples[i-1], "wet") + compute_probability("cloudy", wet_sprinkler_samples[i-1], wet_rain_samples[i-1], "wet"))
    sprinkler_sample_p = compute_probability(wet_sky_samples[i-1], "on", wet_rain_samples[i-1], "wet") / (compute_probability(wet_sky_samples[i-1], "off", wet_rain_samples[i-1], "wet") + compute_probability(wet_sky_samples[i-1], "on", wet_rain_samples[i-1], "wet"))
    rain_sample_p = compute_probability(wet_sky_samples[i-1], wet_sprinkler_samples[i-1], "yes", "wet") / (compute_probability(wet_sky_samples[i-1], wet_sprinkler_samples[i-1], "no", "wet") + compute_probability(wet_sky_samples[i-1], wet_sprinkler_samples[i-1], "yes", "wet"))

    if rand <= sky_sample_p:
        wet_sky_samples.append("cloudy")
    else:
        wet_sky_samples.append("sunny")
    rand = random.uniform(0, 1)
    if rand <= sprinkler_sample_p:
        wet_sprinkler_samples.append("on")
    else:
        wet_sprinkler_samples.append("off")
    rand = random.uniform(0, 1)
    if rand <= rain_sample_p:
        wet_rain_samples.append("yes")
    else:
        wet_rain_samples.append("no")

sum_ = 0
index = 0
for i in sky:
    for j in sprinkler:
        for k in rain:
            count = 0
            for l in range(samples):
                if wet_sky_samples[l] == i and wet_sprinkler_samples[l] == j and wet_rain_samples[l] == k:
                    count = count + 1
            percent_error = 100*abs(count/samples - grass_wet_probabilities[index])
            pe_sig = '%s' % float('%.2g' % percent_error)
            print("gibbs_estimated_probability(sky=" + i + ", sprinkler=" + j + ", rain=" + k , "| grass=wet) =", count/samples, "-> percent error =", pe_sig)
            index = index + 1
            sum_ = sum_ + count/samples
            
print("\n")

# PART D)
print("PART D)")

# I already coded it with strings (cloudy, on, etc.) before this part.
# I am leaving the code above as is and converting into 1s and 0s just for this part: 
for i in range(samples):
    if dry_sky_samples[i] == "cloudy":
        dry_sky_samples[i] = 0
    if dry_sky_samples[i] == "sunny":
        dry_sky_samples[i] = 1
        
    if dry_sprinkler_samples[i] == "on":
        dry_sprinkler_samples[i] = 0
    if dry_sprinkler_samples[i] == "off":
        dry_sprinkler_samples[i] = 1

    if dry_rain_samples[i] == "yes":
        dry_rain_samples[i] = 0
    if dry_rain_samples[i] == "no":
        dry_rain_samples[i] = 1

    if wet_sky_samples[i] == "cloudy":
        wet_sky_samples[i] = 0
    if wet_sky_samples[i] == "sunny":
        wet_sky_samples[i] = 1
        
    if wet_sprinkler_samples[i] == "on":
        wet_sprinkler_samples[i] = 0
    if wet_sprinkler_samples[i] == "off":
        wet_sprinkler_samples[i] = 1

    if wet_rain_samples[i] == "yes":
        wet_rain_samples[i] = 0
    if wet_rain_samples[i] == "no":
        wet_rain_samples[i] = 1

# for dry grass:
dry_samples = [dry_sky_samples, dry_sprinkler_samples, dry_rain_samples]
dry_samples_matrix = corrcoef(dry_samples)
print("Pairwise Correlation Between Gibbs Samples For Dry Grass")
print(dry_samples_matrix)
print()

# for wet grass:
wet_samples = [wet_sky_samples, wet_sprinkler_samples, wet_rain_samples]
wet_samples_matrix = corrcoef(wet_samples)
print("Pairwise Correlation Between Gibbs Samples For Wet Grass")
print(dry_samples_matrix)
