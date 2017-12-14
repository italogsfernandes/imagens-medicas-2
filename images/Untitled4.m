%%
I = imread('liftingbody.png');
I = I(1:end-1,1:end-1);
S = qtdecomp(I,0.27);