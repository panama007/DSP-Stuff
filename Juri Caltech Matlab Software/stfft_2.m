%initial values
close all;
clear all;

%fid=fopen('G25070.dat','r');
fid=fopen('SINUS12.dat','r');
%fid=fopen('chirp.dat','r')

%fid=fopen('SINUS12B.dat','r');

s=fscanf(fid,'%f');
status=fclose(fid);


L=length(s);
Fs=2*pi;
t=0:1/Fs:(L)*1/Fs-1/Fs;
s=s'*10e5; % Amplify for SINUS12 data only

period=L/Fs;

N=length(t);
n=1:N;
frequency=n/N*Fs;

%Original signal

figure;
subplot(3,1,1);
plot(t,s);
axis([0 t(L) -max(abs(s)) max(abs(s))]);
xlabel('Time(sec)')
title('Original Signal');

%Show Window Function
subplot(3,1,2);
plot(t,(10e5)*(1-((t-t(length(t))/2)/5).^2).*exp((-((t-t(length(t))/2)/5).^2)/2),'r');
%change window here
xlabel('Time(sec)')
title('Window Function');

%FFT of original signal
S=fft(s);
S_shift=fftshift(S);
subplot(3,1,3);
plot(frequency-Fs/2,abs(S_shift));
xlabel('Frequency(Centered)')
title('FFT of Original Signal');

%loops for various values of parameters: a and b
for b=10:10:100,
%for b=10:10,
   for a=1:5:25,
   % for a=1:1,
      figure;
      subplot(3,1,1);
      plot(t,s);%
      hold;
      g=(10e5)*(1-((t-b)/a).^2).*exp((-((t-b)/a).^2)/2);
      plot(t,g,'r');
      axis([0 t(L) -max(abs(g)) max(abs(g))]);
      xlabel('Time(sec)')
			title('Original Signal and Window Function');
      hold off;
      
      output=g.*s;
      subplot(3,1,2)
      plot(t,output);
      axis([0 t(L) -max(abs(output)) max(abs(output))]);
      xlabel('Time(sec)')
      title(['Windowed Signal with a=',num2str(a),',b=',num2str(b)]);
      
	 OUTPUT=fft(output);
   OUTPUT_shift=fftshift(OUTPUT);
   subplot(3,1,3);
   plot(frequency-Fs/2,abs(OUTPUT_shift));
   xlabel('Frequency (Centered)')
title('FFT of Windowed Signal');
end;
end;
figure;
specgram(s,[],70,kaiser(256,16));
title('Spectogram of Original Signal');
colormap(bone);

ss=s;
figure;
subplot(2,1,1);
plot(t,ss);
title('Original signal');
xlabel('Time(sec)');

SS=fft(ss);
SS_shift=fftshift(SS);
subplot(2,1,2);
plot(frequency-Fs/2,abs(SS_shift));
title('FFT of original signal');
xlabel('Frequency(Centered)');

figure;
specgram(ss,[],70);
title('Spectogram of signal');
colormap(bone);



