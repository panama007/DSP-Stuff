%  PROGRAM TO CREATE DATA FILES
%
% Number of data points  or number of samples= N (these points may come fron a data acquisition system)
% Sampling(time)period = Ts = 1/N,  in seconds ( 1sec/N-samples).
% If N>> then Ts is << , more samples than necessary for the accurate representation of the analog signal
%                        are extracted from the signal (WASTE of DIGITAL MEMORY).
% If N>> then Ts is << ,less samples are extracted  than necessary for its accurate representation.
% THEREFORE, in order to preserve all the important features of the analog signal N must be sufficiently small. 
% REMEMBER:
% Frequency sampling rate(resolution) = Fs = 1/Ts > to 2*(highest frequency) contained in the analog signal.  
% NOTE: If we choose Fs = 1/(N*Ts) with Ts=1/N, then the frequency sampling resolution is Fs=1hertz.

clear all;

% GLOBAL INPUTS
N=1000;
%N=128;
%N=256;  % Number of data (sample) points
%N=64;
a=2;                                         % Exponent for the exponential decay 

rn=0;                                        % Random noise generation flag ( 0 for no noise and 1 for noise )

%t1=00;										      % Location of the first Dirac delta function on t-axis
%t2=90.0;
t1=128.00;
t2=179.2;80.


%diracdf1=20;										    % Magnitude of the first Dirac delta function
%diracdf2=20;                                  % Magnitude of the second Dirac delta function
%diracdf1=10;
%diracdf2=15;

freq1=10;                                     % Frequencies
freq2=50;
freq3=100;

Ts=1/N;			                              % Sampling(time)interval = delta(t)
                           

t0=0;                                        % Start time  

t=t0:Ts:Ts*(N-1);		                        % delta(t) = 0, 1/N, ... (N-1)/N, 1 



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%sr=1000;   						% Sampling rate
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%sr=10;                                  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%sr=23;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%k=1:N;    										
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%T=k/sr;    


% ADD RANDOM NOISE TO THE SIGNAL

if rn==1 
   
   RN= randn(size(t));
   %RN=0.1*RN;
   RN=1.5*RN;
   figure(1);
   plot(t,RN);
   title('RANDOM NOISE');
   xlabel('Time(sec)')
   ylabel('Amplitude')
else
   RN(1:N)=0.0;   
end;

% SIGNAL GENERATING FUNCTION 

%Name = 'sinefunction';                       % Set the file name 
%Name = 'sum2sines';                    
%Name = 'sum2sinw2dirac';
%Name = 'sum2sinw2broaderdeltas';
Name = 'non-stationary-wave';
%Name = 'suc2sines';
%Name = 'suc3sines';
%%Name = 'OscExpdecay';
%N%ame = 'sintsquare';


%**********************************************************************************************************************
switch Name
   
     case 'sinefunction',       
       
f=sin(2*pi*freq1*t);
%f=f/(2*pi);
%f=cos(2*pi*freq1*t);
%f=sin(2*pi*freq1*t)+RN; 
%specgram(f,256,1e3,256,250);
spectrogram(f);
   
     case 'sum2sines',
   
f=sin(2*pi*freq1*t) + sin(2*pi*freq2*t)+RN;	% Sum of two sine waves of f1 and f2 frequencies
specgram(f,256,1e3,256,250);

     case 'sum2sinw2dirac',
   
f=3*sin(2*pi*freq1*t) + 5*sin(2*pi*freq2*t)+RN;	% Sum of two sine waves of two frequencies with two Dirac Delta functions
                                             % added at times t1 and t2						
f(t1:t1)=f(t1:t1) + diracdf1; 																											
f(t2:t2)=f(t2:t2) + diracdf2;
specgram(f,256,1e3,256,250);

     case 'sum2sinw2broaderdeltas',

f=sin(2*pi*freq1*t)+ sin(2*pi*freq2*t)+RN;						
f(t1:t1+1)=f(t1:t1+1)+diracdf1;
f(t2:t2+1)=f(t2:t2+1)+diracdf1;
specgram(f,256,1e3,256,250);

    case 'non-stationary-wave',

f(1:250)=3*sin(2*pi*freq1*t(1:250));   
f(251:500)=3*sin(2*pi*freq1*t(251:500)) + 5*sin(2*pi*freq2*t(251:500));
f(501:750)=3*sin(2*pi*freq1*t(501:750))+ 5*sin(2*pi*freq2*t(501:750)) + 9*sin(2*pi*freq3*t(501:750));
f(751:1000)=3*sin(2*pi*freq1*t(751:1000));
specgram(f,256,1e3,256,250)

     case 'suc2sines',
   
f(1:256)=sin(2*pi*freq1*t(1:256))+RN(1:256); % Two successive sine waves of  two frequencies
f(257:N)=sin(2*pi*freq2*t(257:N))+RN(257:N); % Signals are separated at t=50 secs
specgram(f,256,1e3,256,250) % Display the spectrogram

     case 'suc3sines',

f(1:170)=sin(2*pi*freq1*t(1:170))+RN(1:170); % Three successive sine waves of  three frequencies
                                          % Signals are separated at t=50 secs
f(171:240)=sin(2*pi*freq2*t(171:240))+RN(171:240); 

f(241:N)=sin(2*pi*freq3*t(241:N))+RN(2411:N); 
specgram(f,256,1e3,256,250)

     case 'chirp',

%t = 0:0.001:256;              % 2 secs @ 1kHz sample rate
%f = chirp(t,0,1,150);       % Start @ DC, cross 150Hz at t=1 sec
%specgram(f,256,1e3,256,250) % Display the spectrogram

t=0:0.1:255;
%f=chirp(t,0,1,10)+RN;  	  					        % Chirp function
%f=chirp(t:0.1:100); 
f=chirp(0.8,t);

specgram(f,256,1e3,256,250) % Display the spectrogram


     case 'OscExpdecay',                          % Oscillating Exponential decay
   
snt=sin(2*pi*freq1*t); 
ex=exp(-a*t);
ddsnt=diag(snt,0);
ddex=diag(ex,0);
RN=RN';
f= diag(ddsnt*ddex)+RN;
specgram(f,256,1e3,256,250)

     case 'sintsquare',
        
f=sin(2*pi*freq1*(t.^2));
specgram(f,256,1e3,256,250)
end;	
%**********************************************************************************************************************   
% PLOTTING THE DATA

figure(2);
plot(t,f);
	
axis([0 t(N) -max(abs(f)) max(abs(f))]);
%title('ORIGINAL SIGNAL');
title('NON-STATIONARY SIGNAL');
xlabel('Time(sec)');
ylabel('Amplitude s(t)');
grid on
%x=0:0.05:5;
%y=sin(x.^2);
%plot(x,y);
%xlabel('Time');
%ylabel('Amplitude');

%figure(3);

%plot(t,f,'.');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%x=N/sr;	
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%axis([0 x -max(abs(f)) max(abs(f))]);
%title('ORIGINAL SIGNAL SAMPLED');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%title('DISCRETE SIGNAL');
%xlabel('Time(sec)');
%ylabel('Amplitude');

ff=f';                                        % Transpose the data row to data column

%%save 'Name'.dat -ascii filaname


response=input('Save File? Go to command window and type 1 for yes and 2 to no ');

if response == 1;

switch Name   
     case 'sinefunction',
   
           save sinefunction.dat -ascii ff;
   
     case 'sum2sines',
   
	        save sum2sines.dat -ascii ff;

     case 'sum2sinw2dirac',
   
           save sum2sinw2dirac.dat -ascii ff;
   
    case 'sum2sinw2broaderdeltas',
   
          save sum2sinw2broaderdeltas.dat -ascii ff;
           
    case 'non-stationary-wave',       
          
           save non-stationary-wave.dat -ascii ff; 
																					
     case 'suc2sines', 

           save suc2sines.dat -ascii ff;

     case 'suc3sines', 

           save suc3sines.dat -ascii ff;

     case 'chirp',
   
           save chirp.dat -ascii ff;
   
     case 'OscExpdecay',
   
           save OscExpdecay.dat -ascii f;
   
     case 'sintsquare',
   
           save sintsquare.dat -ascii ff;


  end;

else
   
end;


% COMMENT 1
% When a signal has two frequency components f1 and f2 the sampling rate should be a least twice 
% the max of f1 and f2.

% COMMENT 2
% To convert the data file generated by this program to an ascii file and save it, type the following
% in Mathlab command window:
% 1. save [newfilename.dat] -ascii [originalfilename].   Example: save twoftwodf.dat -ascii ff 
% 2. copy the data file created to path my .../TestDataGeneration/data
