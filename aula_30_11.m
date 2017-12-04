function aula_30_11()
clear all
close all
im_in = double (imread ('RXjoelho.jpg'));

[rows, cols ] = size ( im_in )
width=rows;
height=cols;

% remover ponto central ( freq = 0 )
mask = zeros ( rows, cols );
%mask ( ceil( rows / 2 ) + 1, ceil( cols / 2 ) + 1 ) = 1;
center_x = width / 2;
center_y = height / 2;
radius = 40;
radius2 = radius ^ 2;
for i = 1 : width
  for j = 1 : height
    dx = i - center_x;
    dy = j - center_y;
    dx2 = dx ^ 2;
    dy2 = dy ^ 2;
    mask(i, j) = dx2 + dy2 <= radius2;
  end;
end;
figure()
imshow(mask)
figure()
DFT  = fft2( im_in );
DFTC = fftshift( DFT );

GC = mask .* DFTC;

G = ifftshift( GC );

im_out = uint8( real ( ifft2 ( G ) ));
im_outDFT  = fft2( im_out );
im_outDFTC = fftshift( im_outDFT );

media = sum ( im_in(:) ) / ( rows * cols )
figure (2);
subplot( 2, 2, 1);imshow( uint8( im_in ) );
subplot( 2, 2, 2);imshow( log ( 1 + abs ( DFTC )) , [3, 10] );
subplot( 2, 2, 3);imshow( im_out );
subplot( 2, 2, 4);imshow( log ( 1 + abs ( im_outDFTC )) , [3, 10] );
