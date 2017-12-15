im = imread('pe.jpg');
figure
imshow(im)
imflat = double(reshape(im, size(im,1) * size(im,2), 1));
classes = 4;
[kIDs, kC] = kmeans(imflat,classes, 'Display', 'iter', 'MaxIter', 50, 'Start', 'sample');
colormap = kC / 256;
imout = reshape(uint8(kIDs), size(im,1), size(im,2));
imout = histeq(imout);
figure
imshow(imout)