%function path, path2 = speed_path(width, height, buoypos, boatLocation, circleBuoy)

filePath = fullfile(fileparts(which('PathPlanningExample')),'data','exampleMaps.mat');
load(filePath)
buoypos = [10 6; 10 13; 40 10]; %array of obstacles %Receive
width = 60; %map x width in meters %Receive
height = 20; %map y heigth in meters %Receive
map = robotics.BinaryOccupancyGrid(width,height,30);
setOccupancy(map, buoypos, 1);
robotRadius = 0.5;
mapInflated = copy(map);
inflate(mapInflated,0.3);
prm = robotics.PRM
%prm2 = robotics.PRM
%prm3 = robotics.PRM
prm4 = robotics.PRM
prm.Map = mapInflated;
%prm2.Map = mapInflated;
%prm3.Map = mapInflated;
prm4.Map = mapInflated;
prm.NumNodes = 300;
%prm2.NumNodes = 100;
%prm3.NumNodes = 100;
prm4.NumNodes = 300;
boatLocation = [8 10]; %xy of the boat %Receive
%gateCenter = [10 13];
circleBuoy = [42 10];
%circleBuoyRight = [42  11];
%circleBuoyLeft = [42 15]; %xy to circle the can %Receive

path = findpath(prm, boatLocation, circleBuoy);
%path2 = findpath(prm2, gateCenter, circleBuoyRight);
%path3 = findpath(prm3, circleBuoyRight, circleBuoyLeft);
path4 = findpath(prm4, circleBuoy, boatLocation);

% Display path
path
%path2
%path3
path4
%end