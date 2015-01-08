h=figure('NumberTitle','off','Name','STFT Time-Frequency Trade-off');
%% Create a signal composed of a few sinusoids
freqs = [ 20, 50]; % in hertz
signalLength = 0.5; % in seconds
Fs  = 1000; % in hertz
t = linspace(0,signalLength,signalLength*Fs);

signal = [];
for i=1:numel(freqs)
    signal = [signal,cos(2*pi*freqs(i)*t)];
end

time = linspace(0,numel(freqs)*signalLength,numel(freqs)*signalLength*Fs);
subplot(3,2,[1 2],'Parent',h);
plot(time,signal);
xlabel('Time (s)')
ylabel('Signal Amplitude (au)')
title(['Signal with '  num2str(numel(freqs)) ' frequency components: ' num2str(freqs) ' Hz']);

%% Demonstrate the frequency-time tradeoff by using variable sized windows
windowSizes = [0.03 0.375]*Fs;
NFFT = 2048;
NOVERLAP = 0;
for i=1:numel(windowSizes)
    [S{i},F{i},T{i}]=spectrogram(signal,windowSizes(i),NOVERLAP,NFFT,Fs);
     ax(i) = subplot(3,2,i+2,'Parent',h); 
    imagesc(T{i},F{i},10*log10(abs(S{i}))); view(0,90); axis('tight');
    ylim([0 200]);
     xlabel('Time (s)'); ylabel('Frequency (Hz');
     title(['Window Size: ' num2str(windowSizes(i)/Fs) ' sec'])
end

%% Continuous wavelet transform
figure(2); 
CWTcoeffs = cwt(signal,1:64,'sym2');
imagesc(time,1:64,abs(CWTcoeffs)); 
axis xy;
xlabel('t'); ylabel('Scales');



