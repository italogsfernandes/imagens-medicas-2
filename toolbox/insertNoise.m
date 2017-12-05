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
%       inputImage: Input image (any type)
%       noiseType: Select one of
%               'Uniform'
%               'Gaussian'
%               'Rayleight'
%               'Exponential'
%               'Gamma'
%               'SaltAndPepper'
%       par: Optional. Cell array with noise specific parameters
%       plotResult: Optional. 'yes' or 'no'. Plot input and output images with
%       respective frequency spectrogram
% 
%   Outputs
%       outputImage: output image (same type as inputImage)
%

function [outputImage] = insertNoise(inputImage, noiseType, plotResult, par)
    %Same type guaranteed
    outputImage = inputImage;
    outputImage = cast(outputImage,class(inputImage));
    switch noiseType
       case 'Uniform'
           if ~exist('par','var')
               par = {0,80};
           end
           uniformNoise = unifrnd(par{1},par{2},size(inputImage));
           outputImage = inputImage + uniformNoise;
           
       case 'Gaussian'
           if ~exist('par','var')
               par = {5,30};
           end
           gaussianNoise = normrnd(par{1},par{2},size(inputImage));
           outputImage = inputImage + gaussianNoise;

       case 'Rayleight'
           if ~exist('par','var')
               par = {20};
           end
           rayleightNoise = raylrnd(par{1},size(inputImage));
           outputImage = inputImage + rayleightNoise;
           
       case 'Exponential'
           if ~exist('par','var')
               par = {5};
           end
           exponentialNoise = exprnd(par{1},size(inputImage));
           outputImage = inputImage + exponentialNoise;
          
       case 'Gamma'
           if ~exist('par','var')
               par = {1,8};
           end
           gammalNoise = gamrnd(par{1},par{2},size(inputImage));
           outputImage = inputImage + gammalNoise;
           
       case 'SaltAndPepper'
           if ~exist('par','var')
               par = {0.05};
           end
           SaltAndPepperNoise = rand(size(inputImage));
           pepperProportion = par{1};
           saltProportion = 1 - pepperProportion;
           pepper = find(SaltAndPepperNoise <= pepperProportion);
           outputImage(pepper) = 0;
           salt = find(SaltAndPepperNoise >= saltProportion);
           %Max value of variable type
           outputImage(salt) = intmax(class(inputImage));
 
       otherwise
          disp('Not valid type');
    end
    
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