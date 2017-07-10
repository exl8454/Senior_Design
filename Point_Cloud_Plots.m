%% Plotting
close all
dotsize = 10;  %adjust as needed

% Raw Data
figure
scatter3(x, y, z, dotsize, z, 'filled');
xlabel('x, [m]')
ylabel('y, [m]')
zlabel('z, [m]')
title('Raw Data')
axis equal
hold
scatter3(0,0,0,'r','linewidth',2)
hold

% Quad Comparision
figure
subplot(2,2,1)
scatter3(x, y, z, dotsize, z, 'filled');
xlabel('x, [m]')
ylabel('y, [m]')
zlabel('z, [m]')
title('Raw Data')
axis equal
hold
scatter3(0,0,0,'r','linewidth',2)
hold

subplot(2,2,2)
scatter3(x_cap, y_cap, z_cap, dotsize, z_cap, 'filled');
xlabel('x, [m]')
ylabel('y, [m]')
zlabel('z, [m]')
format short
title(['Point Reduced Model, ' num2str(Z_lim) ' m ceiling'])
axis equal
hold
scatter3(0,0,0,'r','linewidth',2)
hold

subplot(2,2,3)
scatter3(x_slim, y_slim, z_slim, dotsize, z_slim, 'filled');
xlabel('x, [m]')
ylabel('y, [m]')
zlabel('z, [m]')
title(['NOT WORKING Point Reduced Model, ' num2str(cube*100) ' ^3 cm cube'])
axis equal
hold
scatter3(0,0,0,'r','linewidth',2)
hold

subplot(2,2,4)
scatter3(x_slim_cap, y_slim_cap, z_slim_cap, dotsize, z_slim_cap, 'filled');
xlabel('x, [m]')
ylabel('y, [m]')
zlabel('z, [m]')
title(['NOT WORKING Point Reduced Model, ' num2str(cube*100) ' ^3 cm cube'])
axis equal
hold
scatter3(0,0,0,'r','linewidth',2)
hold