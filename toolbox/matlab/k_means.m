%%  Ronaldo Sena
%   ronaldo.sena@outlook.com
%   December 2017
%   Use it as you please. If we meet some day, and you think
%   this stuff was helpful, you can buy me a beer
%   This script is the one mentioned during the Computerphile's Image
%   Segmentation video by Dr. Mike Pound.
%   
%   Takes a gray-scale input image and performs k-means algorithm on it.
%
%   [outputImage] = averageFilter(inputImage, windowSize, plotResult)
%   
%   Parameters
%       inputImage: input image (any type)
%       classes: split the image in that many classes
%       plotResult: 'yes' or 'no'.
% 
%   Outputs
%       outputImage: output image (same type as inputImage)
% 
%   Note: maximum iterations was set to 100, so don't try to run this using
%   more than a few classes. The output won't be accurate.
%

function [ outputImage ] = k_means( inputImage, classes, plotResult )
    im=inputImage;
    imflat = double(reshape(im, size(im,1) * size(im,2), 1));
    [kIDs] = kmeans(imflat,classes, 'Display', 'iter', 'MaxIter', 100,...
        'Start', 'sample');
    outputImage = reshape(uint8(kIDs), size(im,1), size(im,2));
    outputImage = histeq(outputImage);
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