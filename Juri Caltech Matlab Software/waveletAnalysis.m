function waveletAnalysis(signal,wavType,plotType,nameoffile)

%% Check the input
if nargin<3; plotType = 0;     end; % 0 for 2D and 1 for 3D
if nargin<2; wavType = 'morl'; end
if nargin<1; error('[Error] Please provide an input'); end

%% Create the interface
h=figure('NumberTitle','off','Name', ['Wavelet Analysis: ' wavType]);
ax(1)  = subplot(3,2,1); % Plot the original signal here
ax(3)  = subplot(3,2,[3 5]); % Plot the slice from the scalogram here
ax(4)  = subplot(3,2,6); % Display the peaks of the slice here
ax(5)  = subplot(3,2,4); % Display the fourier transform of the slice here
params.wavType = wavType;
params.plotType = plotType;

% Wavelet types
winTypes = {'morl','mexh','db1'};
plotTypes = {'2D','3D'};

% Wavelet parameters
params.scales = 1:128;


% Plot the original signal
plot(ax(1),signal);
xlabel(ax(1),'Time (s)');
ylabel(ax(1),'Amplitude (au)');
title(ax(1), ['Original Signal:' nameoffile]);
xaxis = [0 length(signal)];
xlim(ax(1),[0 length(signal)]);

% Compute the continuous wavelet transform
CWTcoeffs = cwt(signal,params.scales,params.wavType); 
axes(ax(3)); imagesc(abs(CWTcoeffs));
axis xy;
ylim(ax(3),[1 max(params.scales)]);
xlim(ax(3),[0 length(signal)]);
title(ax(3),'sqrt(Re(coeffs)^2 + Im(coeffs^2))');
xlabel(ax(3),'Time (s)');
ylabel(ax(3),['Scales: ' num2str(params.scales(1)) ':' num2str(params.scales(end)) ]);
colormap jet;


% Get a slice from the scalogram
set(h,'windowbuttondownfcn',{@mouseclick_callback,CWTcoeffs,ax,xaxis})

% Create the controls
wavType = uicontrol('Style', 'popup','String', ...
                     'morl|mexh|db1',...
                     'Position',...
                     [300 20 80 20]);                  
plotType = uicontrol('Style', 'popup','String', ...
                     '2D|3D',...
                     'Position',... 
                     [200 20 80 20]);                    
scalesSlider = uicontrol('Style', 'slider',...
                         'Min',2,'Max',360,'Value',128,...
                         'Position',  [100 20 80 20]); 
control(1) = uicontrol('Style','pushbutton',...
                       'String', 'Save Figure',...
                       'Position',[400 20 100 20],...
                       'Callback',@savefigure);                 
 while true
        
          
          % Check to see if anything is changed, only plot if there is a
          flags(1) = ~strcmp(winTypes{get(wavType,'Value')},params.wavType);
          flags(2) = ~strcmp(plotTypes{get(plotType,'Value')},params.plotType);
          flags(3) = ~(round(get(scalesSlider,'Value'))==params.scales(end));
          

          if flags(3)
              params.scales = 1:round(get(scalesSlider,'Value'));
              CWTcoeffs = cwt(signal,params.scales,params.wavType); 
              axes(ax(3)); imagesc(abs(CWTcoeffs));
              ylim(ax(3),[1 max(params.scales)]);
              xlim(ax(3),[0 length(signal)]);
              title(ax(3),'sqrt(Re(coeffs)^2 + Im(coeffs^2))');
              xlabel(ax(3),'Time (s)');
              ylabel(ax(3),['Scales: ' num2str(params.scales(1)) ':' num2str(params.scales(end)) ]);
              
          end
          
            
          % Change the wavetype
          if flags(1)
              params.wavType =winTypes{get(wavType,'Value')};
              CWTcoeffs = cwt(signal,params.scales,params.wavType); 
              axes(ax(3)); imagesc(abs(CWTcoeffs));
              ylim(ax(3),[1 max(params.scales)]);
              xlim(ax(3),[0 length(signal)]);
              title(ax(3),'sqrt(Re(coeffs)^2 + Im(coeffs^2))');
              xlabel(ax(3),'Time (s)');
              ylabel(ax(3),['Scales: ' num2str(params.scales(1)) ':' num2str(params.scales(end)) ]);
              set(h,'windowbuttondownfcn',{@mouseclick_callback,CWTcoeffs,ax,xaxis})

          end
          
          if flags(2)
              
              if get(plotType,'Value')==2
                  cla(ax(3));
                  surf(CWTcoeffs);
                  shading interp;
                  ylim(ax(3),[1 max(params.scales)]);
                  xlim(ax(3),[0 length(signal)]);
                  title(ax(3),'sqrt(Re(coeffs)^2 + Im(coeffs^2))');
                  xlabel(ax(3),'Time (s)');
                  ylabel(ax(3),['Scales: ' num2str(params.scales(1)) ':' num2str(params.scales(end)) ]);

              end
              
              if get(plotType,'Value')==1
                 cla(ax(3)); 
                 imagesc(abs(CWTcoeffs));
                 axis xy 
                 ylim(ax(3),[1 max(params.scales)]);
                 title(ax(3),'sqrt(Re(coeffs)^2 + Im(coeffs^2))');
                 xlabel(ax(3),'Time (s)');
                 ylabel(ax(3),['Scales: ' num2str(params.scales(1)) ':' num2str(params.scales(end)) ]);

              end
          end
          
          if any(flags)
             set(h,'windowbuttondownfcn',{@mouseclick_callback,CWTcoeffs,ax,xaxis})
          end
       
       pause(0.5);
       drawnow;      
end                
              
                 
end

function  mouseclick_callback(varargin)
% WindowButtonDownFcn for figure.
clickLocation = get(gca,'CurrentPoint');
whichWavelet = round(clickLocation(1,2));

% Plot the slice from the scalogram
slice = abs(varargin{3}(whichWavelet,:));
plot(varargin{4}(5),slice);
title(varargin{4}(5),['Selected wavelet, Scale = ' num2str(whichWavelet),', Time = ' num2str(clickLocation(1,1))]);
xlabel(varargin{4}(5),'Time (s)')
ylabel(varargin{4}(5),'Magnitude');
xlim(varargin{4}(5),varargin{5});
hold(varargin{4}(5),'on');
[pks,locs] = findpeaks(slice);
plot(varargin{4}(5),locs,pks,'xr');
hold(varargin{4}(5),'off');

% Plot the peak values in a table
cnames = {'Time','Magnitude'};
temp = num2cell(1:numel(locs));
tableLocation = [0.57,0.71,0.18,0.22];
rownames = cellfun(@(x) num2str(x),temp,'UniformOutput',false);
uitable('Parent',gcf,'Data',[locs',pks'],'ColumnName',cnames,... 
            'RowName',rownames,'units','normalized','Position',tableLocation);

% Plot the fourier transfrom of the slice
NFFT = 2^nextpow2(length(slice));
Y = fft(slice,NFFT);
Y = abs(Y(1:NFFT/2 +1));
f = linspace(0,pi,NFFT/2 +1);
plot(varargin{4}(4),f,Y);
title(varargin{4}(4),'Fourier Coefficients');
xlabel(varargin{4}(4),'Normalized frequency (radians)')
ylabel(varargin{4}(4),'Magnitude');
xlim(varargin{4}(4),[min(f),max(f)]);
[pks_fft,locs_fft] = findpeaks(Y);

% Eliminate peaks that are less than 50% of the max
idx_eliminate = pks_fft<0.5*max(pks_fft);
pks_fft(idx_eliminate) = [];
locs_fft(idx_eliminate) = [];

% Plot the peaks in the same figure
hold(varargin{4}(4),'on');
plot(varargin{4}(4),f(locs_fft),pks_fft,'xr');
hold(varargin{4}(4),'off');

% Plot the peak values in a table
cnames = {'Frequency','Magnitude'};
temp = num2cell(1:numel(locs_fft));
tableLocation = [0.76,0.76,0.16,0.17];
rownames = cellfun(@(x) num2str(x),temp,'UniformOutput',false);
uitable('Parent',gcf,'Data',[f(locs_fft)',pks_fft'],'ColumnName',cnames,... 
            'RowName',rownames,'units','normalized','Position',tableLocation);

end

% Callback functions
function savefigure(hObj,event)
str = datestr(clock);
saveas(hObj,str,'png');
end




