%%  Ronaldo Sena
%   ronaldo.sena@outlook.com
%   September 2017
%   Use it as you please. If we meet some day, and you think
%   this stuff was helpful, you can buy me a beer

% Caminho a partir desta pasta para a pasta onde estão as imagens
% utilizadas
addpath('../../datasets') 
clear;
clc;
close all;

%%  First part

fileName = {'arteriaBMP.bmp','blood0.PNG','blood1.PNG','pe.jpg'};
inImages = {uint8(1:length(fileName))};
outImages = {uint8(1:length(fileName))};
brightness = 100;

for i = 1:length(fileName);
    inImages{i} = imread(fileName{i});
end

for i = 1:length(fileName);
    outImages{1,i} = inImages{i} + brightness;
    outImages{2,i} = inImages{i} - brightness;
%     outImages{3,i} = inImages{i} .* 1.2;
    
    figure(i);
    set(figure(i), 'Position', get(0, 'Screensize'));
        
    subplot(2,3,1)
    imshow(inImages{i});
    title('Original')
    subplot(2,3,4)
    imhist(inImages{i});
    title('Histograma original')
    
    subplot(2,3,2)
    imshow(outImages{1,i});    
    title(['Brilho aumentado de ', int2str(brightness)]);
    subplot(2,3,5)
    imhist(outImages{1,i});    
    title(['Histograma do brilho aumentado de ', int2str(brightness)]);
    
    subplot(2,3,3)
    imshow(outImages{2,i});
    title(['Brilho diminuido de ', int2str(brightness)]);
    subplot(2,3,6)
    imhist(outImages{2,i});    
    title(['Histograma do brilho diminuido de ', int2str(brightness)]);
end
input('Press to continue...');

%%  Second part

for i = 1:length(fileName);
    outImages{3,i} = inImages{i} .* 1.2;
    
    figure(i);
    set(figure(i), 'Position', get(0, 'Screensize'));
        
    subplot(2,2,1)
    imshow(inImages{i});
    title('Original')
    subplot(2,2,3)
    imhist(inImages{i});
    title('Histograma original')
    
    subplot(2,2,2)
    imshow(outImages{3,i});
    title('Constraste alterado')
    subplot(2,2,4)
    imhist(outImages{3,i});
    title('Histograma alterado')
end