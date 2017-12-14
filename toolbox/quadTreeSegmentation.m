%%  Ronaldo Sena
%   ronaldo.sena@outlook.com
%   December 2017
%   Use it as you please. If we meet some day, and you think
%   this stuff was helpful, you can buy me a beer
%
%    quadTreeSegmentation performs a tree segmentation on input image. Tree
%    segmentation segments the input image in squares with similar pixels
%
%   [outputImage] = quadTreeSegmentation(inputImage,plotResult) 
%   
%   Parameters
%       inputImage------: input image (any type)
%       plotResult------: 'yes' or 'no'. Plot input and output images with
%       respective frequency spectrogram
% 
%   Outputs
%       outputImage-----: output image (same type as inputImage)
%

function [outputImage] = quadTreeSegmentation(inputImage,plotResult)

    %This is really bad implementation, but in order to do quadtree
    %segmentation, one must assure that the image is a power of 2. So... if
    %anyone ever read this, please, do it in a more elegant way.
    
    [rows, cols] = size (inputImage);
    if rows > cols
        disp('Not square image');
        toPad = rows - cols;
        padding = zeros(rows,round(toPad/2));        
        inputImage = [padding,inputImage,padding];
    elseif cols > rows
        disp('Not square image');
        toPad = cols - rows;
        padding = zeros(round(toPad/2),cols);
        inputImage = [padding;inputImage;padding];
    end
    %triming excess
    [rows, cols] = size (inputImage);
    if rows>cols
       inputImage = inputImage(1:end-1,:); 
    elseif cols>rows
        inputImage = inputImage(:,1:end-1); 
    end
    %at this point, the image is a square
    r = rem(sqrt(length(inputImage)),2);
    %if not a perfect square
    if r ~= 0
        toPad = abs(pow2(nextpow2(length(inputImage))) - length(inputImage));
        padding = zeros(round(toPad/2),length(inputImage));
        inputImage = [padding;inputImage;padding];
        padding = zeros(length(inputImage),round(toPad/2));
        inputImage = [padding,inputImage,padding];        
    end
    
    %So, I belive this code will run for every image size
    
    S = qtdecomp(inputImage,.27);
    outputImage = repmat(uint8(0),size(S));

    for dim = [512 256 128 64 32 16 8 4 2 1];    
      numblocks = length(find(S==dim));    
      if (numblocks > 0)        
        values = repmat(uint8(1),[dim dim numblocks]);
        values(2:dim,2:dim,:) = 0;
        outputImage = qtsetblk(outputImage,S,dim,values);
      end
    end

    outputImage(end,1:end) = 1;
    outputImage(1:end,end) = 1;    
    
    if ~exist('plotResult','var')
        plotResult = 'no';
    end
    if strcmp(plotResult,'yes')
        figure ();
        im1 = subplot (1,2,1);
        imshow (inputImage);
        title 'Input Image'
        im2 = subplot (1,2,2);
        imshow(outputImage,[]);
        title 'Output Image' 
        linkaxes([im1,im2],'xy')
    end
end