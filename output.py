from turtle import *
color('black')
speed(0)
mem=[]
pd();fd(10.0);
mem.append((pos(), heading()));
right(40.0);
pd();fd(10.0);
pu();tmp=mem.pop();goto(tmp[0]);seth(tmp[1]);
pd();fd(10.0);
mem.append((pos(), heading()));
left(40.0);
pd();fd(10.0);
pu();tmp=mem.pop();goto(tmp[0]);seth(tmp[1]);
mem.append((pos(), heading()));
right(40.0);
pd();fd(10.0);
pu();tmp=mem.pop();goto(tmp[0]);seth(tmp[1]);
pd();fd(10.0);
exitonclick();