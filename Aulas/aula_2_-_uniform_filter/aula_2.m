%%  Ronaldo Sena
%   ronaldo.sena@outlook.com
%   September 2017
%   Use it as you please. If we meet some day, and you think
%   this stuff was helpful, you can buy me a beer

% Caminho a partir desta pasta para a pasta onde estão as imagens
% utilizadas
addpath('../../datasets') 

%%  First part
clear;
clc;
close all;

fileName = {'arteriaBMP.bmp','blood0.PNG','blood1.PNG','pe.jpg'};
inImages = {uint8(1:length(fileName))};
outImages = {uint8(1:length(fileName))};
brightness = 100;
maskSize = {3,7,25};

for i = 1:length(maskSize)
    filter{i} = fspecial('average',maskSize{i});
end
for i = 1:length(fileName)
    inImages{i} = imread(fileName{i});
    figure(i);
    set(figure(i), 'Position', get(0, 'Screensize'));
    subplot(2,length(maskSize)+1,1)
    imshow(inImages{i});
    title('Original')
    subplot(2,length(maskSize)+1,length(maskSize)+2)
    imhist(inImages{i});
    title('Histograma original')
    
    for j = 1:length(maskSize)        
        outImages{i,j} = imfilter(inImages{i},filter{j});
        subplot(2,length(maskSize)+1,(j+1))
        imshow(outImages{i,j});
        title(['Máscara de ',int2str(maskSize{j}),'x',int2str(maskSize{j})])
        subplot(2,length(maskSize)+1,j+length(maskSize)+2)
        imhist(outImages{i,j});
        title(['Histograma com máscara de ',int2str(maskSize{j}),'x',int2str(maskSize{j})])
    end
end
input('Press to continue...');