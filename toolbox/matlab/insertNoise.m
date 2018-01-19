%%  Ronaldo Sena
%   ronaldo.sena@outlook.com
%   December 2017
%   Use it as you please. If we meet some day, and you think
%   this stuff was helpful, you can buy me a beer
%   Shout out to professor Ana Claudia, for the inspiring code
% 
%   Ideal high pass filter. Takes in an image and a mask size and
%   oupts the filtered image in same type as original one
% 
%   [outputImage] = idealHighPass(inputImage, radius, plotResult) 
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
%   Use example:
%       Insert 2% of noise in the image, (1% salt and 1% pepper)
%          outputImage = insertNoise(inputImage, 'SaltAndPepper', 'yes',{0.01});
% 
%       By default, insert 10% of noise in the image, (5% salt and 5% pepper)
%          outputImage = insertNoise(inputImage, 'SaltAndPepper');
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
           try
               uniformNoise = unifrnd(par{1},par{2},size(inputImage));
               uniformNoise = cast(uniformNoise,class(inputImage));
               outputImage = inputImage + uniformNoise;
           catch
               disp('Invalid noise parameters');
           end
           
       case 'Gaussian'
           if ~exist('par','var')
               par = {5,30};
           end
           try
               gaussianNoise = normrnd(par{1},par{2},size(inputImage));
               gaussianNoise = cast(gaussianNoise,class(inputImage));
               outputImage = inputImage + gaussianNoise;
           catch
               disp('Invalid noise parameters');
           end

       case 'Rayleight'
           if ~exist('par','var')
               par = {20};
           end
           try
               rayleightNoise = raylrnd(par{1},size(inputImage));
               rayleightNoise = cast(rayleightNoise,class(inputImage));
               outputImage = inputImage + rayleightNoise;
           catch
               disp('Invalid noise parameters');
           end
           
       case 'Exponential'
           if ~exist('par','var')
               par = {5};
           end
           try
               exponentialNoise = exprnd(par{1},size(inputImage));
               exponentialNoise = cast(exponentialNoise,class(inputImage));
               outputImage = inputImage + exponentialNoise;
           catch
               disp('Invalid noise parameters');
           end
           
       case 'Gamma'
           if ~exist('par','var')
               par = {1,8};
           end
           try
               gammalNoise = gamrnd(par{1},par{2},size(inputImage));
               gammalNoise = cast(gammalNoise,class(inputImage));
               outputImage = inputImage + gammalNoise;
           catch
               disp('Invalid noise parameters');
           end           
           
       case 'SaltAndPepper'
           if ~exist('par','var')
               par = {0.05};
           end
           try
               SaltAndPepperNoise = rand(size(inputImage));
               pepperProportion = par{1};
               saltProportion = 1 - pepperProportion;
               pepper = find(SaltAndPepperNoise <= pepperProportion);
               outputImage(pepper) = 0;
               salt = find(SaltAndPepperNoise >= saltProportion);
               %Max value of variable type
               outputImage(salt) = intmax(class(inputImage));
           catch
               disp('Invalid noise parameters');
           end  
 
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