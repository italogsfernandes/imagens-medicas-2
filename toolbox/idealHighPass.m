%%  Ronaldo Sena
%   ronaldo.sena@outlook.com
%   December 2017
%   Use it as you please. If we meet some day, and you think
%   this stuff was helpful, you can buy me a beer
%   Shout out to professor Ana Claudia, for the inspiring code
%
%   Ideal high pass filter. Takes a image and the mask radius and
%   oupts the filtered image in same type
%
%   [outputImage] = idealHighPass(inputImage, radius, verbose) 
%   
%   Parameters
%       inputImage: input image (any type)
%       radius: radius of ideal filter
%       plotResult: 'yes' or 'no'. Plot input and output images with
%       respective frequency spectrogram
% 
%   Outputs
%       outputImage: output image (same type as inputImage)
%

function [outputImage] = idealHighPass(inputImage, radius, plotResult)    
    [rows, cols] = size (inputImage);
    if radius > min(rows,cols)
        radius = min(rows,cols);
    end      
    mask = zeros(rows,cols);
    %'Drawing' a circle
    radius = radius^2;  
    centerX = rows/2;
    centerY = cols/2;
    for i = 1 : rows
        for j = 1 : cols
            dx = i - centerX;
            dx = dx^2;
            dy = j - centerY;
            dy = dy^2;
            mask(i, j) = dx + dy >= radius;
        end;
    end;    
    %Calculating FFT 
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