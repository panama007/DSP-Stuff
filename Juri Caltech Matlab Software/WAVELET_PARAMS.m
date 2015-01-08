% N = 1024;
% t = linspace(0,1,N);
% t = 0:0.001:2;            % 2 secs @ 1kHz sample rate
% signal = chirp(t,0,1,10);
% signal = 4*sin(2*pi*8*t).*(t<=0.5)+sin(2*pi*16*t).*(t>0.5);
% signal = sin(2*pi*8*t)+sin(2*pi*16*t);


%% COMMENT: THIS FUNCTION WORKS ON VERSIONS OF MATLAB THAT ARE GREATER THAN
%% 2013b
%%                             

%filename = 'G31722.DAT';
filename = 'G31710.DAT';
%filename = 'G31211.DAT';
%filename = 'G32181.DAT';
%filename = 'G32170.DAT';
%filename = 'G42388.DAT';
%filename = 'G29361.DAT';
%filename = 'G43506.DAT';
%filename = 'G43495.DAT';
y=load(filename);
Fs =2500;
% Take the first 60ms
signal = y(1:Fs*60/1e3);
wavType = {'morl','haar','mexh','db1','sym'};
waveletAnalysis(signal,wavType{1},0,filename);