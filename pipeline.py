from regress import data
from helper import *
from montecarlo import *
import math

#PS 1
print "Problem Set 2\n======================================="
print "Problem 5\n---------------------------------------"

print "b)"
ps_one = data('csv/wage2.csv')
beta = ps_one.regression('wage',['educ','Constant'])
print "Regression of wages on education and a constant"
print "Beta on education: " + str(beta[0])


beta = ps_one.regression('lwage',['educ','Constant'])
print "\nRegression of lgwage on education and a constant"
print "Beta on education: " + str(beta[0])

print "\nc)"
corr = ps_one.correlation(['educ','exper'])
print "Correlation Matrix"
print "\t\teducation\texperience"
print "education\t" + str(corr[0][0]) + "\t\t" + str(corr[0][1])
print "experience\t" + "\t\t" + str(corr[1][1])


beta = ps_one.regression('lwage',['educ','Constant','exper'])
print "\nRegression of lgwage on education, experience, and a constant"
print "Beta on education: " + str(beta[0])

print "\nd)"
ps_one.gen('lgIQ', math.log, 'iq')
beta = ps_one.regression('lwage',['lgIQ','Constant'])
print "\nRegression of lgwage on lgIQ and a constant"
print "Beta on lgIQ: " + str(beta[0])

print "\ne)"
beta = ps_one.regression('lwage',['educ','exper','iq','Constant'])
print "\nRegression of lgwage on education, experience, IQ and a constant"
print "Beta on education: " + str(beta[0])

ps_one.gen('IQ2',square,'iq')
beta = ps_one.regression('lwage',['educ','exper','iq','IQ2','Constant'])
print "\nRegression of lgwage on education, experience, IQ, IQ^2 and a constant"
print "Beta on education: " + str(beta[0])

print "\nf)"
beta = ps_one.regression('lwage',['educ','exper','kww','Constant'])
print "\nRegression of lgwage on education, experience, KWW and a constant"
print "Beta on education: " + str(beta[0])

ps_one.gen('lgkww',math.log,'kww')
beta = ps_one.regression('lwage',['educ','exper','lgkww','Constant'])
print "\nRegression of lgwage on education, experience, lgKWW and a constant"
print "Beta on education: " + str(beta[0])

ps_one.gen('kww2',square,'kww')
beta = ps_one.regression('lwage',['educ','exper','kww','kww2','Constant'])
print "\nRegression of lgwage on education, experience, KWW, KWW^2 and a constant"
print "Beta on education: " + str(beta[0])

beta = ps_one.regression('lwage',['educ','exper','kww','iq','Constant'])
print "\nRegression of lgwage on education, experience, KWW, IQ and a constant"
print "Beta on education: " + str(beta[0])


# ===================================================================================
print "Problem Set 3\n======================================="
print "Problem 5\n---------------------------------------"

print "b)"
d = data('csv/wagepan2.csv')
beta = d.regression('lwage',['educ',"Constant"])
print "\nRegression of lgwage on education and a constant"
print "Beta on education: " + str(beta[0])

print "\nc)"
print "\nPooled regression of lgwage on education and a constant with year as unit"
print "Beta on education(overall): " + str(beta[0])
beta = d.indicator_regression('lwage','year',['educ',"Constant"])
for val,b in beta.iteritems():
	print "Beta on education(year " + str(val) + "): " + str(b[0])

# print "\nd)"
# beta = d.fixed_effects('lwage','nr','year',['educ','Constant'])
# print beta

print "\ne)"
beta = d.regression('lwage',['Constant','union'])
print "\nRegression of lgwage on union and a constant"
print "Beta on education: " + str(beta[0])

print "\nf)"
d.gen('exper2',square,'exper')
beta = d.regression('lwage',['union','manuf','exper','exper2','Constant'])
print "\nRegression of lgwage on union, manufacturing,  experience, experience^2 and a constant"
print "Beta on education: " + str(beta[0])

# print "Problem 6\n---------------------------------------"
# print "b) Standard Dev: " + str(MC(0.0,1.0,0.0,0.0,0.3,1.0,2.0,2.0)[1])
# print "c) Standard Dev: " + str(MC(0.0,1.0,0.0,0.0,0.3,1.0,2.0,1.0)[1])
# print "d) Standard Dev: " + str(MC(0.0,1.0,0.0,0.0,0.3,1.0,1.5,2.0)[1])
# print "e) Standard Dev: " + str(MC(0.0,0.0,0.0,0.0,0.3,1.0,2.0,2.0)[1])
# print "f) Standard Dev: " + str(MC(0.0,1.0,0.0,0.0,0.0,1.0,2.0,2.0)[1])
