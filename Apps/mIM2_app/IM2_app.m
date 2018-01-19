%%  Ronaldo Sena
%   ronaldo.sena@outlook.com
%   December 2017
%   Use it as you please. If we meet some day, and you think
%   this stuff was helpful, you can buy me a beer
%   Shout out to professor Ana Claudia, for the inspiring code
% 
%   GUI to process medical images



% 
%   
%                       CONFIGURAÇÕES INCIAIS
%
% 
function varargout = IM2_app(varargin)
% IM2_APP MATLAB code for IM2_app.fig
%      IM2_APP, by itself, creates a new IM2_APP or raises the existing
%      singleton*.
%
%      H = IM2_APP returns the handle to a new IM2_APP or the handle to
%      the existing singleton*.
%
%      IM2_APP('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in IM2_APP.M with the given input arguments.
%
%      IM2_APP('Property','Value',...) creates a new IM2_APP or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before IM2_app_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to IM2_app_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help IM2_app

% Last Modified by GUIDE v2.5 25-Dec-2017 21:40:39

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @IM2_app_OpeningFcn, ...
                   'gui_OutputFcn',  @IM2_app_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT

% --- Executes just before IM2_app is made visible.
function IM2_app_OpeningFcn(hObject, eventdata, handles, varargin)
global raio ordem limiarArvore limiarCrescimento limiarKmeans ...
    mascara seeds comparar segmentar filtrar Kclasses seedsInv;
handles.output = hObject;
% set(handles.panel_filtros,'visible','off')
% set(handles.panel_segmentacao,'visible','on')
raio = str2double(handles.text_raio.String);
ordem = str2double(handles.text_ordem.String);
comparar = 0;
segmentar = 0;
filtrar = 1;
limiarArvore = 0.27;
limiarCrescimento = 0.27;
limiarKmeans = 0.27;
mascara = str2double(handles.text_mascara.String);
Kclasses = 3;
seeds = [];
seedsInv = [];
handles.panel_filtros.Visible = 'on';
handles.panel_segmentacao.Visible = 'off';
% Caminho a partir desta pasta para a pasta onde estão as imagens
% utilizadas
addpath('../../toolbox/matlab') 
% Update handles structure
guidata(hObject, handles);

function varargout = IM2_app_OutputFcn(hObject, eventdata, handles) 
varargout{1} = handles.output;

function edit2_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
% 
%   
%                       CONFIGURAÇÕES INCIAIS
%
% 



% 
%   
%                       INSERIR RUIDOS
%
% 
function pushbutton_salEpimenta_Callback(hObject, eventdata, handles)
global imagemSaida comparar;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
imagemSaida = insertNoise(imagemSaida,'SaltAndPepper',plotResult);
axes(handles.axes_saida);
imshow(imagemSaida);

function pushbutton_gamma_Callback(hObject, eventdata, handles)
global imagemSaida comparar;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
imagemSaida = insertNoise(imagemSaida,'Gamma',plotResult);
axes(handles.axes_saida);
imshow(imagemSaida);

function pushbutton_exponential_Callback(hObject, eventdata, handles)
global imagemSaida comparar;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
imagemSaida = insertNoise(imagemSaida,'Exponential',plotResult);
axes(handles.axes_saida);
imshow(imagemSaida);

function pushbutton_rayleight_Callback(hObject, eventdata, handles)
global imagemSaida comparar;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
imagemSaida = insertNoise(imagemSaida,'Rayleight',plotResult);
axes(handles.axes_saida);
imshow(imagemSaida);

function pushbutton_gaussiano_Callback(hObject, eventdata, handles)
global imagemSaida comparar;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
imagemSaida = insertNoise(imagemSaida,'Gaussian',plotResult);
axes(handles.axes_saida);
imshow(imagemSaida);

function pushbutton_uniforme_Callback(hObject, eventdata, handles)
global imagemSaida comparar;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
imagemSaida = insertNoise(imagemSaida,'Uniform',plotResult);
axes(handles.axes_saida);
imshow(imagemSaida);
% 
%   
%                       INSERIR RUIDOS
%
% 




%
%   
%                       FILTROS ESPACIAIS
% 
%
function pushbutton_media_Callback(hObject, eventdata, handles)
global imagemSaida comparar mascara;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
[imagemSaida] = averageFilter(imagemSaida, mascara,plotResult); 
axes(handles.axes_saida);
imshow(imagemSaida);

function pushbutton_mediana_Callback(hObject, eventdata, handles)
global imagemSaida comparar mascara;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
[imagemSaida] = medianFilter(imagemSaida, mascara,plotResult); 
axes(handles.axes_saida);
imshow(imagemSaida);

function pushbutton_minimo_Callback(hObject, eventdata, handles)
global imagemSaida comparar mascara;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
[imagemSaida] = minimumFilter(imagemSaida, mascara,plotResult); 
axes(handles.axes_saida);
imshow(imagemSaida);

function pushbutton_maximo_Callback(hObject, eventdata, handles)
global imagemSaida comparar mascara;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
[imagemSaida] = maximumFilter(imagemSaida, mascara,plotResult); 
axes(handles.axes_saida);
imshow(imagemSaida);
%
%   
%                       FILTROS ESPACIAIS
% 
%




%
%   
%                       CONFIGURAÇÕES
% 
%
function text_mascara_Callback(hObject, eventdata, handles)
global mascara;
mascara = str2double(get(hObject,'String'));

function text_mascara_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function pushbutton_carregar_Callback(hObject, eventdata, handles)
global imagemSaida imagemEntrada;
[FileName,PathName] = uigetfile({'*.*',  'All Files (*.*)'}, ...
        'Escolha uma imagem');
imagemEntrada = imread([PathName FileName]);
imagemSaida = imagemEntrada;
axes(handles.axes_saida);
imshow(imagemSaida);
axes(handles.axes_original);
imshow(imagemEntrada);
linkaxes([handles.axes_original,handles.axes_saida],'xy')

function pushbutton_reset_Callback(hObject, eventdata, handles)
global imagemEntrada imagemSaida seeds seedsInv;
imagemSaida = imagemEntrada;
axes(handles.axes_saida);
cla
axes(handles.axes_original);
cla
axes(handles.axes_saida);
imshow(imagemSaida);
axes(handles.axes_original);
imshow(imagemEntrada);
seeds = [];
seedsInv = [];

function radiobutton_filtragem_Callback(hObject, eventdata, handles)
if get(hObject,'Value')    
    handles.panel_segmentacao.Visible = 'off';
    handles.panel_filtros.Visible = 'on';    
end    

function radiobutton_segmentacao_Callback(hObject, eventdata, handles)
if get(hObject,'Value')    
    set(handles.panel_filtros,'visible','off')
    set(handles.panel_segmentacao,'visible','on')
end    

function radiobutton_comparar_Callback(hObject, eventdata, handles)
global comparar;
comparar =  get(hObject,'Value');
%
%   
%                       CONFIGURAÇÕES
% 
%




%
%   
%                       FILTROS DE FREQUÊNCIA
% 
%
function pushbutton_ideal_Callback(hObject, eventdata, handles)
global raio imagemSaida comparar;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
if handles.radiobutton_passaAlta.Value
    tipo = 'high';
elseif handles.radiobutton_passaBaixa.Value
    tipo = 'low';
end
[imagemSaida] = idealFilter(imagemSaida, tipo, raio, plotResult);
axes(handles.axes_saida);
imshow(imagemSaida);


function pushbutton_butter_Callback(hObject, eventdata, handles)
global raio ordem imagemSaida comparar;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
if handles.radiobutton_passaAlta.Value
    tipo = 'high';
elseif handles.radiobutton_passaBaixa.Value
    tipo = 'low';
end
[imagemSaida] = butterworthFilter(imagemSaida,tipo,raio,ordem,plotResult); 
axes(handles.axes_saida);
imshow(imagemSaida);

function pushbutton_gauss_Callback(hObject, eventdata, handles)
global raio imagemSaida comparar;
if comparar == 0
    plotResult = 'no';
else
    plotResult = 'yes';
end
if handles.radiobutton_passaAlta.Value
    tipo = 'high';
elseif handles.radiobutton_passaBaixa.Value
    tipo = 'low';
end
[imagemSaida] = gaussianFilter(imagemSaida,tipo,raio,plotResult); 
axes(handles.axes_saida);
imshow(imagemSaida);
    
function text_raio_Callback(hObject, eventdata, handles)
global raio;
raio = str2double(get(hObject,'String'));

function text_raio_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function text_ordem_Callback(hObject, eventdata, handles)
global ordem;
ordem = str2double(get(hObject,'String'));

function text_ordem_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
%
%   
%                       FILTROS DE FREQUÊNCIA
% 
%




%
%   
%                       SEGMENTAÇÃO
% 
%
% --- Executes on button press in pushbutton_lancarSementes.
function pushbutton_lancarSementes_Callback(hObject, eventdata, handles)
global seeds seedsInv imagemSaida imagemMarcada;
imagemMarcada = [];
% Hint: get(hObject,'Value') returns toggle state of checkbox_sementes
p = ginput(1);
y = round(axes2pix(size(imagemSaida, 2), get(handles.axes_original.Children, 'XData'), p(2)));
x = round(axes2pix(size(imagemSaida, 1), get(handles.axes_original.Children, 'YData'), p(1)));
seeds = [seeds; [x y]];
disp('xablaus');
imagemMarcada = insertMarker(imagemSaida,seeds);
% inverte para proxima funcao
seedsInv = [seedsInv; [y x]];
axes(handles.axes_saida);
imshow(imagemMarcada);

function pushbutton_arvore_Callback(hObject, eventdata, handles)
global imagemSaida limiarArvore;
quadTreeSegmentation(imagemSaida',limiarArvore,'yes');

function pushbutton_crescimento_Callback(hObject, eventdata, handles)
global seedsInv imagemSaida limiar;
limiarCrescimento = round(limiar*255);
% imagemMarcada = handles.axes_input.Children.CData;
axes(handles.axes_saida);
cla
imshow(imagemSaida);
for i=1:size(seedsInv,1);    
    poly = regionGrowing(imagemSaida, [seedsInv(i,:) 1], limiarCrescimento);
    hold on    
    plot(poly(:,1), poly(:,2), 'LineWidth', 2)
end
hold off

function pushbutton_kmeans_Callback(hObject, eventdata, handles)
global Kclasses imagemSaida;
k_means(imagemSaida,Kclasses,'yes');

function slider_arvore_Callback(hObject, eventdata, handles)
global limiarArvore;
limiarArvore = get(hObject,'Value');
set(handles.label_arvore,'String',num2str(limiarArvore));

function slider_arvore_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end

function slider_kmeans_Callback(hObject, eventdata, handles)
global limiarKmeans;
limiarKmeans = get(hObject,'Value');
set(handles.label_kmeans,'String',num2str(limiarKmeans));

function slider_kmeans_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end

function slider_crescimento_Callback(hObject, eventdata, handles)
global limiarCrescimento;
limiarCrescimento = get(hObject,'Value');
set(handles.label_crescimento,'String',num2str(limiarCrescimento));

function slider_crescimento_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end

function text_classes_Callback(hObject, eventdata, handles)
global Kclasses;
Kclasses = str2double(get(hObject,'String'));

function text_classes_CreateFcn(hObject, eventdata, handles)
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
%
%   
%                       SEGMENTAÇÃO
% 
%



function pushbutton_histograma_Callback(hObject, eventdata, handles)
global imagemEntrada imagemSaida;
figure ();
im1 = subplot (1,2,1);
imhist(imagemEntrada); 
title 'Input Image'
im2 = subplot (1,2,2);
imhist(imagemSaida); 
title 'Output Image'
linkaxes([im1,im2],'xy')

function pushbutton_equalizar_Callback(hObject, eventdata, handles)
global imagemSaida;
imagemSaida = histeq(imagemSaida);
axes(handles.axes_saida);
imshow(imagemSaida);
