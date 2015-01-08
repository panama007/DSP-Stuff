% Visual display of all the steps involved in computing the short-fourier
% transform of a given signal

function stft(filename,Fs)

% Check inputs
if nargin<2; Fs = 2*pi; end
if nargin<1; error('Need to specify signal source'); end

% Read the signal, compute the time scale over which it evolves
signal = readfile(filename)';
len    = length(signal);
time   = linspace(0,len/Fs,len);


% Spectrogram Parameters
winSize = 256;
sigBlock = 1:winSize;

% FFT parameters
NFFT = 2^nextpow2(winSize); % Next power of 2 from length of y
f = Fs/2*linspace(0,1,NFFT/2+1);

% Window Types
winTypes = {'mexhat','gaussian','rect','gabor'};


% Window parameters
params.winType = 'mexhat';
params.LB = -5;
params.UB = 5;
params.sigma=1;
params.winSize = winSize;

% Initialize the figure
figure('NumberTitle','off','Name','Iterative STFT','Position',[321 56 997 736]);
ax(1) = subplot(4,4,[1 2]); % Plot original signal here
ax(2) = subplot(4,4,5); % Plot windowed signal here
ax(4) = subplot(4,4,9); % Plot the FFT of the windowed signal here
ax(5) = subplot(4,4,6); % plot the windowed signal
ax(6) = subplot(4,4,[3 4 7 8 11 12 15 16]); % plot the spectrogram
ax(7) = subplot(4,4,10);% plot the reconstruction of the signal
ax(8) = subplot(4,4,[13 14]); % plot the fft of the entire signal


winType = uicontrol('Style', 'popup','String', ...
                     'mexican hat|gaussian|rectangular',...
                     'Position', [300 20 120 20]);    
                 
winSigma = uicontrol('Style', 'slider',...
        'Min',0.5,'Max',1.5,'Value',1,...
        'Position', [500 20 120 20]);
    
uicontrol('Style','text',...
        'Position',[500 45 120 20],...
        'String','Window Sigma');
    
winSizeHandle = uicontrol('Style', 'slider',...
        'Min',64,'Max',1024,'Value',256,...
        'Position', [100 20 120 20]);
    
uicontrol('Style','text',...
        'Position',[100 45 120 20],...
        'String','Window Size');   

winPosition = uicontrol('Style', 'slider',...
        'Min',1,'Max',len,'Value',1,...
        'Position', [700 20 120 20]);
    
uicontrol('Style','text',...
        'Position',[700 45 120 20],...
        'String','Window Position');  
    
    
% Plot for the first time

window = genWindow(params);


% Original signal with winSize overlayed
plot(ax(1),time,signal); 
hold(ax(1),'on');

plot(ax(1),time(sigBlock),signal(sigBlock),'r','LineWidth',3);
xlabel(ax(1),'Time (s)');
ylabel(ax(1),'Signal Amplitude (AU)');
title(ax(1),'Original Signal');
axis(ax(1),'tight');
hold(ax(1),'off');

% Plot the window used to segment the signal
plot(ax(2),window);
axis(ax(2),'tight');
title('Window used to segment signal');

% Compute the windowed signal
windowed=window.*signal(sigBlock);

% Plot the single sided fourier transform
windowedFFT = fft(windowed,NFFT)/winSize;
plot(ax(4),f,abs(windowedFFT(1:NFFT/2+1)));
xlabel(ax(4),'Frequency (Centered)')
ylabel(ax(4),'|FFT(signal)|');
title(ax(4),'log of FFT of Windowed Signal');
axis(ax(4),'tight');

% Plot the reconstruction
plot(ax(5),time(sigBlock),windowed,'b');
title(ax(5),'Windowed Signal');
axis(ax(5),'tight');

% Plot the reconstruction
plot(ax(7),time(sigBlock),ifft(winSize*windowedFFT),'r');
title(ax(7),'IFFT reconctruction');
axis(ax(7),'tight');


% Plot the FFT of the whole signal
nrFreqSamples = min([2^nextpow2(length(signal)) 1024]);
f = Fs/2*linspace(0,1,nrFreqSamples/2+1);
%wholeSignalFFT = fft(signal,nrFreqSamples)/length(signal); % normalized
wholeSignalFFT = fft(signal,nrFreqSamples);
plot(ax(8),f,abs(wholeSignalFFT(1:nrFreqSamples/2+1)));
title(ax(8),'FFT of entire signal');
xlabel(ax(8),'Frequency (Hz)');
ylabel(ax(8),'|FFT(signal)|');
axis(ax(8),'tight');
    
    
while (sigBlock(end)<len)
    
          % Check to see if anything is changed, only plot if there is a
          % change
          flags(1) = ~isequal(sigBlock,get(winPosition,'Value'):sigBlock(1)+winSize-1);
          flags(2) = ~isequal(get(winSigma,'Value'),params.sigma);
          flags(3) = ~isequal(get(winSizeHandle,'Value'),winSize);
          flags(4) = ~strcmp(winTypes{get(winType,'Value')},params.winType);
    
          
          if any(flags)

              % Update parameters
              params.winType = winTypes{get(winType,'Value')};
              params.sigma = get(winSigma,'Value');
              winSize = 2^nextpow2(get(winSizeHandle,'Value'));
              NFFT = winSize;
              f = Fs/2*linspace(0,1,NFFT/2+1);
              params.winSize = winSize;
              window = genWindow(params);
              sigBlock = round(get(winPosition,'Value')):round(get(winPosition,'Value'))+winSize-1;

              if (sigBlock(end)<len)

                  % Original signal with winSize overlayed
                  plot(ax(1),time,signal); 
                  hold(ax(1),'on');


                  plot(ax(1),time(sigBlock),signal(sigBlock),'r','LineWidth',3);
                  xlabel(ax(1),'Time (s)');
                  ylabel(ax(1),'Signal Amplitude (AU)');
                  title(ax(1),'Original Signal');
                  axis(ax(1),'tight');
                  hold(ax(1),'off');

                  % Plot the window used to segment the signal
                  plot(ax(2),window);
                  axis(ax(2),'tight');
                  title('Window used to segment signal');

                  % Compute the windowed signal
                  windowed=window.*signal(sigBlock);

                 % Plot the single sided fourier transform
                 % windowedFFT = fft(windowed,NFFT)/winSize; % normalized
                  windowedFFT = fft(windowed,NFFT);
                  plot(ax(4),f,abs(windowedFFT(1:NFFT/2+1)));
                  xlabel(ax(4),'Frequency (Centered)')
                  ylabel(ax(4),'|FFT(signal)|');
                  title(ax(4),'log of FFT of Windowed Signal');
                  axis(ax(4),'tight');

                  % Plot the reconstruction
                  plot(ax(5),time(sigBlock),windowed,'b');
                  title(ax(5),'Windowed Signal');
                  axis(ax(5),'tight');

                    % Plot the reconstruction
                  plot(ax(7),time(sigBlock),ifft(winSize*windowedFFT),'r');
                  title(ax(7),'IFFT reconctruction');
                  axis(ax(7),'tight');
                  
                 % Plot the spectrogram
                  S = getSpectrogram(signal,window,NFFT,winSize,Fs);
                  axes(ax(6));
                  imagesc(abs(S));
                  
                  
              else
                  break;
              end

          end
          
          drawnow;
end

axes(ax(6));
spectrogram(signal,winSize,round(0.8*winSize),2^nextpow2(len),Fs);
title(ax(6),'Spectrogram of Signal');
% figure;
% [S,F,T] = spectrogram(signal,winSize,round(0.8*winSize),2^nextpow2(len),Fs);
% surf(T,F,10*log(abs(S)))
end

function signal = readfile(filename)
fid=fopen(filename,'r');
signal=fscanf(fid,'%f');
fclose(fid);
end

function window = genWindow(params)
winType = params.winType;
LB = params.LB;
UB = params.UB;
N = params.winSize;
out2 = linspace(LB,UB,N);
sigma = params.sigma;

switch winType
    
    case 'mexhat'
         out1 = (out2/sigma).^2;
         window = (2/(sqrt(3)*sigma*pi^0.25))*exp(-out1/(2*sigma^2)).* (1-out1);   
         
    case 'gaussian'
        
          window =1/sqrt(2*pi*sigma^2)*exp(-out2.^2/sigma^2);
          window = window./norm(window); 
          
    case 'rect'
        
          window = ones(1,length(out2));
          window = window./norm(window);
     
end

end

function S = getSpectrogram(signal,window,NFFT,winSize,Fs)
        
      % Time vector
      
        
      % Pad the signal
        paddedSignal = [zeros(1,winSize),signal,zeros(1,winSize)];
        center = winSize+1;
        iter = 0;
      while center<length(signal)
            iter = iter +1;
            extract = center-winSize/2:center+winSize/2-1;
            windowedSignal = paddedSignal(extract).*window;
            temp =fft(windowedSignal,NFFT); 
            S(iter,:) =temp(1:NFFT/2+1);
            center = center + winSize;
      end

end







