%{ 
    1. Internal
       -Provide a function handle
    2. External
       -Provide a filename
%}


function signal = genSignal(type,params)


switch type
    case 'intern'
        functionHandle = params.funHandle;
        inputSpace = params.inputSpace;
        signal = functionHandle(inputSpace);    
    case 'extern'
        if isfield(params,filename)
            [~,~,ext] = fileparts(params.filename);
            switch ext
                case '.mat'
                    signal = load(params.filename);
                case '.dat'
                    fid=fopen(filename,'r');
                    signal=fscanf(fid,'%f');
                    fclose(fid);
            end
        else
            warning('[WARNING] Please provide a filename')
        end
end
