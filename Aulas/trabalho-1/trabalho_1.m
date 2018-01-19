%% Ronaldo Sena
%  ronaldo.sena@outlook.com
%  October 2017
%  Use it as you please. If we meet some day, and you think
%  this stuff was helpful, you can buy me a coffee... or a beer

%%  First part
% Caminho a partir desta pasta para a pasta onde estão as imagens
% utilizadas
addpath('../../datasets') 

clear;
clc;
close all;

fileName = {'arteriaBMP.bmp','blood0.PNG','blood1.PNG','pe.jpg'};
inImages = {uint8(1:length(fileName))};
outImages = {uint8(1:length(fileName))};
maskSize = {3};

for i = 1:length(maskSize)
    filter{i} = fspecial('average',maskSize{i});
end

%%  Processing
for i = 1:length(fileName)
    inImages{i} = imread(fileName{i});
    %First cell line will be the equalized image
    outImages{i,1} = histeq(inImages{i});
    %Then the equalized image will be filtered by a 3x3 filter mask
    outImages{i,2} = imfilter(outImages{i,1},filter{1});
    %Finaly, the original image also will be filtered by a 3x3 filter mask
    outImages{i,3} = imfilter(inImages{i},filter{1});
end

%%  Plotting
for i = 1:length(fileName)
    figure(i);
    set(figure(i), 'Position', get(0, 'Screensize'));
    subplot(2,3,1)
    imshow(inImages{i});
    title('Original')
    subplot(2,3,4)
    imhist(inImages{i});
    title('Histograma original')

    subplot(2,3,2)
    imshow(outImages{i,1});
    title('Equalizada')
    subplot(2,3,5)
    imhist(outImages{i,1});
    title('Histograma Equalizado')
    
    subplot(2,3,3)
    imshow(outImages{i,2});
    title(['Mascara de ',int2str(maskSize{1}),'x',int2str(maskSize{1})])
    subplot(2,3,6)
    imhist(outImages{i,2});
    title(['Histograma com mascara de ',int2str(maskSize{1}),'x',int2str(maskSize{1})])
end