%%  Ronaldo Sena
%   ronaldo.sena@outlook.com
%   December 2017
%   Use it as you please. If we meet some day, and you think
%   this stuff was helpful, you can buy me a beer
%   Shout out to professor Ana Claudia, for the inspiring code
%
%   Minimum filter implementation using MATLAB's processing toolbox
%
%   [outputImage] = maximumFilter(inputImage, windowSize, plotResult)
%   
%   Parameters
%       inputImage: input image (any type)
%       windowSize: mask size
%       plotResult: 'yes' or 'no'. Plot input and output images with
%       respective frequency spectrogram
% 
%   Outputs
%       outputImage: output image (same type as inputImage)
%

function [outputImage] = minimumFilter(inputImage, windowSize, plotResult)
    %Using processing toolbox
    outputImage = imerode(inputImage, true(windowSize));
    %Same type guaranteed
    outputImage = cast(outputImage,class(inputImage));
    
    if ~exist('plotResult','var')
        plotResult = 'no';
    end
    if strcmp(plotResult,'yes')
        figure ();
        im1 = subplot (1,2,1);
        imshow (inputImage); 
        title 'Input Image'
        im2 = subplot (1,2,2);
        imshow (outputImage); 
        title 'Output Image'
        linkaxes([im1,im2],'xy')
    end
end