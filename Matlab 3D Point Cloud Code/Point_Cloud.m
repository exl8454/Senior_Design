

thetaD=theta+91.2;      %Shifts frame
thetaR=thetaD*pi/180;   %Converts to radians
phiD=phi-0;             %Shifts frame
phiR=phi*pi/180;        %Converts to radians
R=r/1000;               %Converts to Meters


%Raw Data
[x,y,z]=sph2cart(phiR,thetaR,R);
%z=z-min(z);    %shifts frame
Raw=[x y z];

%Ceiling filter
Z_lim=.925*max(z);
k=1;
for i=1:size(x)
    
    if z(i)>Z_lim
        
        %don't save
        
    else
        x_cap(k,1)=x(i);
        y_cap(k,1)=y(i);
        z_cap(k,1)=z(i);
        k=k+1;
    end
end

Cap = [x_cap y_cap z_cap];

%% NOT WORKING Sliming Data file Raw
cube=0.01;       %1 cm

j=1;

for i=1:size(x)

    for k=i+1:size(x)
        
        if (abs(x(i)-x(k))<cube) && (abs(y(i)-y(k))<cube) && (abs(z(i)-z(k))<cube)  
            keep=false;
            break
        else
            keep=true;
        end
        
    end
    
    if keep == true
        
       x_slim(j)=x(i); 
       y_slim(j)=y(i); 
       z_slim(j)=z(i); 
       j=j+1;
       
    end
    
end

slim=[x_slim y_slim z_slim];

%% NOT WORKING Sliming Data file Cap
j=1;

for i=1:size(x_cap)

    for k=i+1:size(x_cap)
        
        if (abs(x_cap(i)-x_cap(k))<cube) && (abs(y_cap(i)-y_cap(k))<cube) && (abs(z_cap(i)-z_cap(k))<cube)  
            keep=false;
            break
        else
            keep=true;
        end
        
    end
    
    if keep == true
        
       x_slim_cap(j)=x_cap(i); 
       y_slim_cap(j)=y_cap(i); 
       z_slim_cap(j)=z_cap(i); 
       j=j+1;
       
    end
    
end

slim_cap=[x_slim_cap y_slim_cap z_slim_cap];


Point_Cloud_Plots

clearvars phiD phiR thetaD thetaR R x x_cap x_slim x_slim_cap y y_cap y_slim x_slim_cap z z_cap z_slim z_slim_cap i j k  