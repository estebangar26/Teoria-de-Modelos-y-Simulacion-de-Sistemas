%% Sistema de Primer Orden
% Este sistema se da cuando L=0: H(s)=1/(tao*s+lambda)
t=linspace(0,0.8,100);
R=1; % cmH_2O s/ l
C=0.1;% l/cmH_2O
lambda=2;% Lazo cerrado
HLA=tf(1,[R*C 1]);
HLC=tf(1,[R*C lambda]);
% En lazo abierto y en lazo cerrado
y1=impulse(HLA,t); y2=impulse(HLC,t); figure(1);
plot(t,y1,'b',t,y2,'r--','linewidth',2); xlabel('tiempo (s)'); ylabel('Respuesta al Impulso'); 
legend('Lazo Abierto','Lazo Cerrado');
axis([-0.1 0.8 0 11]); axis square; hold on; stem(0,10,'k')
% Respuesta al escalón
y1=step(HLA,t); y2=step(HLC,t); figure(2);
plot(t,y1,'b',t,y2,'r--','linewidth',2); xlabel('tiempo (s)'); ylabel('Respuesta al Escalón'); 
legend('Lazo Abierto','Lazo Cerrado');
axis([-0.1 0.8 0 1]); axis square; 