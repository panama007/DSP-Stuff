% Read the data
filename = 'G25070.dat';
fid=fopen(filename,'r');
signal=fscanf(fid,'%f');
fclose(fid);

Fs = 2500;
subplot(3,1,1); plot(signal)
subplot(3,1,2); plot(abs(fftshift(fft(signal))));