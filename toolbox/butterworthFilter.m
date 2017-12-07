%%  Ronaldo Sena
%   ronaldo.sena@outlook.com
%   December 2017
%   Use it as you please. If we meet some day, and you think
%   this stuff was helpful, you can buy me a beer
%
%   Butterworth filter. Takes an image and the mask radius and
%   oupts the filtered image in same type
%
%   [outputImage] = butterworhtFilter(inputImage,type,radius,order,plotResult) 
%   
%   Parameters
%       inputImage------: input image (any type)
%       type------------: 'low' for low-pass or 'high' for high-pass
%       radius----------: filter radius
%       order-----------: radius of ideal filter
%       plotResult------: 'yes' or 'no'. Plot input and output images with
%       respective frequency spectrogram
% 
%   Outputs
%       outputImage-----: output image (same type as inputImage)
%

function [outputImage] = butterworthFilter(inputImage,type, radius,...
                                            order,plotResult)
    [rows, cols] = size (inputImage);
    if radius > min(rows,cols)
        radius = min(rows,cols);
    end
    [x,y] = meshgrid(-floor(cols/2):floor(cols-1)/2, ...
                     -floor(rows/2):floor(rows-1)/2);
	%Butterworth transfer function
    if strcmp(type,'high')
        mask = 1./(1.+((radius./(x.^2+y.^2).^0.5).^(2*order)));
    elseif strcmp(type,'low')
        mask = 1./(1.+(((x.^2+y.^2).^0.5./radius).^(2*order)));
    end

    DFT  = fft2(inputImage);
    DFTC = fftshift(DFT);    
    GC = mask .* DFTC;
    G = ifftshift(GC);
    outputImage = real(ifft2(G));
    %Same type guaranteed
    outputImage = cast(outputImage,class(inputImage));    
    
    if ~exist('plotResult','var')
        plotResult = 'no';
    end
    if strcmp(plotResult,'yes')
        figure()
        imshow(mask)
        title 'Mask used'
        figure ();
        im1 = subplot (2,2,1);
        imshow (inputImage);
        title 'Input Image'
        subplot (2,2,2);
        imshow (log(1+abs(DFTC)) , [3, 10]); 
        title 'Input Image FFT'
        im2 = subplot (2,2,3);
        imshow (outputImage); 
        title 'Output Image'
        subplot (2,2,4);
        imshow (log(1+abs(GC)) , [3, 10]); 
        title 'Output Image FFT'
        linkaxes([im1,im2],'xy')
    end
end

