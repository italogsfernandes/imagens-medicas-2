# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLANDIA
# Faculty of Electrical Engineering
# Biomedical Engineering Lab
# ------------------------------------------------------------------------------
# Author: Italo Gustavo Sampaio Fernandes
# Contact: italogsfernandes@gmail.com
# Git: www.github.com/italogfernandes
# ------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------
import sys

import matplotlib.pyplot as plt  # Showing images
# ------------------------------------------------------------------------------
import numpy as np  # Images are handled as nparray
# ------------------------------------------------------------------------------
# PyQt5
# from PyQt5.QtWidgets import *
# from views import base_qt5 as base
# PyQt4
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
# ------------------------------------------------------------------------------
from matplotlib.figure import Figure
from scipy import misc  # Opening images

from controllers import image_handler as ih
from views import base_qt4 as base
# ------------------------------------------------------------------------------
sys.path.append('../../toolbox/python')
import scipy_toolbox  # Custom toolbox with image processing functions
# ------------------------------------------------------------------------------


class IM2APP(QMainWindow, base.Ui_MainWindow):
    def __init__(self, parent=None):
        super(IM2APP, self).__init__(parent)
        self.setupUi(self)
        # region Initializing the attributes
        self.my_history = []
        # endregion
        # region Images and Matplotlib Figures
        self.original_image = np.ones((100, 100), dtype=np.uint8) * 127
        self.edited_image = np.copy(self.original_image)
        self.undo_backup_image = np.copy(self.edited_image)
        self.original_image_fig = Figure(figsize=(0.1, 0.1))
        self.original_image_canvas = FigureCanvas(self.original_image_fig)
        self.edited_image_fig = Figure(figsize=(0.1, 0.1))
        self.edited_image_canvas = FigureCanvas(self.edited_image_fig)
        self.edited_image_toolbar = NavigationToolbar(self.edited_image_canvas, self, coordinates=True)
        # endregion
        # region Ui setup
        self.pos_setup_ui()
        self.setup_signals_connections()
        self.pos_signals_ui()
        # endregion

    # region UI SETUP
    def replace_ui_widgets(self):
        # self.statusbar.hide()
        self.lbl_fixed_status.hide()
        self.lbl_status_msg.hide()
        # region Image viewers
        self.v_layout_edited_image.removeWidget(self.replace_edited_image)
        self.h_layout_original_image.removeWidget(self.replace_original_image)
        self.replace_edited_image.setParent(None)
        self.replace_original_image.setParent(None)

        self.original_image_canvas.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.original_image_canvas.updateGeometry()
        self.h_layout_original_image.addWidget(self.original_image_canvas)
        self.original_image_canvas.draw()

        self.edited_image_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.edited_image_canvas.updateGeometry()
        self.v_layout_edited_image.addWidget(self.edited_image_canvas)
        self.edited_image_canvas.draw()
        self.v_layout_edited_image.addWidget(self.edited_image_toolbar)
        # endregion

    def pos_setup_ui(self):
        self.replace_ui_widgets()
        self.update_original_figure()
        self.update_edited_figure()
        # region Menus
        # TODO: scipy_toolbox.format_names
        # TODO: ajustar escala: 0,1 - 0,255 - -1,1
        # TODO: color / rgb selection
        self.cb_format.addItems(('uint8',
                                 'float64'))
        self.sl_brightness.setRange(-100, 100)
        self.sl_contrast.setRange(0, 100)

        self.cb_noise.addItems(scipy_toolbox.noise_names)
        self.sl_noise_amount.setRange(0, 1000)

        self.cb_filter.addItems(scipy_toolbox.filter_names)
        self.sl_filter_size.setRange(1, 50)

        self.cb_morph_type.addItems(scipy_toolbox.mathematical_morphologies_names)
        self.sl_morph_size.setRange(1, 50)

        self.sl_segmentation_th.setRange(0, 255)
        # endregion

    def pos_signals_ui(self):
        self.cb_format.setCurrentIndex(0)
        self.cb_noise.setCurrentIndex(1)
        self.cb_filter.setCurrentIndex(1)
        self.cb_morph_type.setCurrentIndex(1)

    def setup_signals_connections(self):
        # region Basics Menu
        self.cb_format.currentIndexChanged.connect(self.cb_img_format_changed)
        self.btn_format.clicked.connect(self.btn_apply_img_format_clicked)
        self.sl_brightness.valueChanged.connect(self.sl_brightness_value_changed)
        self.btn_brightness.clicked.connect(self.btn_apply_brightness_clicked)
        self.sl_contrast.valueChanged.connect(self.sl_contrast_value_changed)
        self.btn_contrast.clicked.connect(self.btn_apply_contrast_clicked)
        # endregion
        # region Noise Menu
        self.cb_noise.currentIndexChanged.connect(self.cb_noise_changed)
        self.sl_noise_amount.valueChanged.connect(self.sl_noise_amount_changed)
        self.btn_insert_noise.clicked.connect(self.btn_noise_clicked)
        # endregion
        # region Filter Menu
        self.cb_filter.currentIndexChanged.connect(self.cb_filter_changed)
        self.sl_filter_size.valueChanged.connect(self.sl_filter_size_changed)
        self.btn_insert_filter.clicked.connect(self.btn_insert_filter_clicked)
        # endregion
        # region Mathematical Morphologies Menu
        self.cb_morph_type.currentIndexChanged.connect(self.cb_morph_type_changed)
        self.radio_morph_binary.toggled.connect(self.radio_morph_binary_gray_toggled)
        # self.radio_morph_grey.toggled.connect(self.radio_morph_binary_gray_toggled)
        self.sl_morph_size.valueChanged.connect(self.sl_morph_size_value_changed)
        self.btn_morph.clicked.connect(self.btn_apply_morph_clicked)
        # endregion
        # region Segmentation Menu
        self.sl_segmentation_th.valueChanged.connect(self.sl_segmentation_threshold_value_changed)
        self.radio_seg_mean_th.toggled.connect(self.radio_mean_median_toggled)
        self.radio_seg_median_th.toggled.connect(self.radio_mean_median_toggled)
        self.btn_hist_segmentation.clicked.connect(self.btn_apply_segmentation_clicked)
        # endregion
        # region Misc Menu
        self.btn_labels.clicked.connect(self.btn_labels_clicked)
        # endregion
        # region Option Menu
        self.btn_equalize.clicked.connect(self.btn_equalize_clicked)
        self.radio_compare.clicked.connect(self.radio_compare_clicked)
        self.radio_hist.clicked.connect(self.radio_hist_clicked)
        # endregion
        # region Action Menu Bar
        self.actionAbrir.triggered.connect(self.action_open_triggered)
        self.actionReset.triggered.connect(self.action_reset_triggered)
        self.actionUndo.triggered.connect(self.action_undo_triggered)
        self.actionVer_Historico.triggered.connect(self.action_see_history_triggered)
        self.actionSalvar_em_docx.triggered.connect(self.action_save_in_doc_triggered)
        self.menuSobre.addAction('&About', self.about)
        # endregion

    # endregion

    # region Interface Slots
    # region Basics Menu
    def cb_img_format_changed(self):
        image_format = self.cb_format.currentText()
        self.lbl_format.setText('Formato: %s' % image_format)

    def btn_apply_img_format_clicked(self):
        image_format = self.cb_format.currentText()
        d_type = np.uint8
        if image_format == 'uint8':
            d_type = np.uint8
        elif image_format == 'float64':
            d_type = np.float64
        mod = ih.ImageModifier('basic', 'format', {'dtype': d_type})
        self.apply_modifier(mod)

    def sl_brightness_value_changed(self):
        self.lbl_brightness.setText("Brilho: %d" % self.sl_brightness.value())

    def btn_apply_brightness_clicked(self):
        mod = ih.ImageModifier('basic', 'brightness', {'level': self.sl_brightness.value()})
        self.apply_modifier(mod)

    def sl_contrast_value_changed(self):
        self.lbl_contrast.setText('Contrast: %d' % self.sl_contrast.value())

    def btn_apply_contrast_clicked(self):
        mod = ih.ImageModifier('basic', 'contrast', {'level': self.sl_contrast.value()})
        self.apply_modifier(mod)

    # endregion

    # region Noise Menu
    def cb_noise_changed(self):
        noise_type = str(self.cb_noise.currentText())
        self.lbl_noise.setText('Ruído: ' + noise_type)
        noise_params = scipy_toolbox.noise_params[noise_type].copy()
        noise_amount = noise_params.pop('amount')
        self.lbl_noise_amount.setText('Multiplier: %.3f' % noise_amount)
        self.sl_noise_amount.setValue(noise_amount * 1000)
        self.lbl_noise_params.setText('Params: %s' %
                                      ', '.join([str(p) for p in noise_params.keys()]))
        self.edit_noise_params.setText(', '.join([str(p) for p in noise_params.values()]))

    def sl_noise_amount_changed(self):
        noise_amount = self.sl_noise_amount.value() / 1000.0
        self.lbl_noise_amount.setText('Multiplier: %.3f' % noise_amount)

    def btn_noise_clicked(self):
        keys = self.lbl_noise_params.text().split(': ')
        if len(keys) > 1:
            keys = [k for k in keys[1].split(', ')]
        else:
            keys = []

        values = [float(param) for param in self.edit_noise_params.text().split(', ')]

        keys.append('amount')
        values.append(self.sl_noise_amount.value() / 1000.0)

        d = {}
        for i in range(len(keys)):
            d[keys[i]] = values[i]

        mod = ih.ImageModifier('noise', self.cb_noise.currentText(), d)
        self.apply_modifier(mod)

    # endregion

    # region Filter Menu
    def cb_filter_changed(self):
        filter_type = str(self.cb_filter.currentText())
        self.lbl_filter.setText('Filtro: ' + filter_type)
        filter_params = scipy_toolbox.filter_params[filter_type].copy()
        if 'size' in filter_params.keys():
            self.lbl_filter_size.show()
            self.sl_filter_size.show()
            filter_size = filter_params.pop('size')
            self.lbl_filter_size.setText('Size(px): %d' % filter_size)
            self.sl_filter_size.setValue(filter_size)
        else:
            self.lbl_filter_size.hide()
            self.sl_filter_size.hide()

        if not filter_params == {}:
            self.lbl_filter_params.show()
            self.edit_filter_params.show()
            self.lbl_filter_params.setText('Params: %s' % ', '.join([str(p) for p in filter_params.keys()]))
            self.edit_filter_params.setText(', '.join([str(p) for p in filter_params.values()]))
        else:
            self.lbl_filter_params.hide()
            self.edit_filter_params.hide()

    def sl_filter_size_changed(self):
        filter_size = self.sl_filter_size.value()
        self.lbl_filter_size.setText('Size(px): %d' % filter_size)

    def btn_insert_filter_clicked(self):
        keys = []
        values = []
        if not self.lbl_filter_params.isHidden():
            keys = self.lbl_filter_params.text().split(': ')
            if len(keys) > 1:
                keys = [k for k in keys[1].split(', ')]
            else:
                keys = []
            values = [float(param) for param in self.edit_filter_params.text().split(', ')]

        if not self.sl_filter_size.isHidden():
            keys.append('size')
            values.append(self.sl_filter_size.value())

        d = {}
        for i in range(len(keys)):
            d[keys[i]] = values[i]

        mod = ih.ImageModifier('filter',
                               self.cb_filter.currentText(), d)
        self.apply_modifier(mod)

    # endregion

    # region Mathematical Morphologies Menu
    def cb_morph_type_changed(self):
        self.label_morph_type.setText("Morph: %s" % self.cb_morph_type.currentText())

    def radio_morph_binary_gray_toggled(self):
        pass

    def sl_morph_size_value_changed(self):
        self.lbl_morph_size.setText("Size(px): %d" % self.sl_morph_size.value())

    def btn_apply_morph_clicked(self):
        morph_name = self.cb_morph_type.currentText()
        morph_op = 'binary' if self.radio_morph_binary.isChecked() else 'grey'
        morph_size = self.sl_morph_size.value()
        d = {'morph_op': morph_op, 'size': morph_size}
        mod = ih.ImageModifier('morphology', morph_name, d)
        print(mod)
        self.apply_modifier(mod)

    # endregion

    # region Segmentation Menu
    def sl_segmentation_threshold_value_changed(self):
        self.lbl_seg_threshold.setText('Limiar: %d' % self.sl_segmentation_th.value())
        self.radio_seg_median_th.setChecked(False)
        self.radio_seg_mean_th.setChecked(False)

    def radio_mean_median_toggled(self):
        if self.radio_seg_mean_th.isChecked():
            self.sl_segmentation_th.setValue(self.edited_image.mean())
        elif self.radio_seg_median_th.isChecked():
            self.sl_segmentation_th.setValue(self.edited_image.max() - self.edited_image.min())

    def btn_apply_segmentation_clicked(self):
        mod = ih.ImageModifier('segmentation', 'histogram',
                               {'threshold': self.sl_segmentation_th.value()})
        self.apply_modifier(mod)

    # endregion

    # region Misc Menu
    def btn_labels_clicked(self):
        from scipy import ndimage
        import matplotlib.pyplot as plt
        self.undo_backup_image = self.edited_image
        label_im, nb_labels = ndimage.label(self.edited_image)
        self.btn_labels.setText("Labels: %d" % nb_labels)  # how many regions?
        plt.imshow(label_im)
        plt.title('Regioes Econtradas: %d' % nb_labels)
        plt.show()

    def do_example_labels(self):
        """
        Modifier: noise - salt_and_pepper - {'s_vs_p': 0.5, 'amount': 0.004}
        Modifier: morphology - dilation - {'morph_op': 'grey', 'size': 10}
        Modifier: filter - gaussian - {'sigma': 3.0}
        Modifier: segmentation - histogram - {'threshold': 148}
        """
        pass

    # endregion

    # region Option Menu
    def btn_equalize_clicked(self):
        self.edited_image = ih.equalize_image(self.edited_image)
        self.update_edited_figure()

    def radio_compare_clicked(self):
        self.update_edited_figure()

    def radio_hist_clicked(self):
        self.update_edited_figure()

    # endregion

    # region Actions Menu Bar
    def action_open_triggered(self):
        dlg = QFileDialog(self)
        dlg.setWindowTitle('Secione a imagem que deseja abrir.')
        dlg.setViewMode(QFileDialog.Detail)
        file_name = dlg.getOpenFileName(self, 'Open File')
        self.original_image = misc.imread(file_name, mode='L').astype(np.float64)
        print(self.original_image.dtype)
        self.edited_image = np.copy(self.original_image)
        self.setWindowTitle('Medical Images App' + file_name)
        self.update_original_figure()
        self.update_edited_figure()

    def action_reset_triggered(self):
        self.edited_image = np.copy(self.original_image)
        self.update_edited_figure()

    def action_undo_triggered(self):
        self.actionUndo.setEnabled(False)
        self.my_history.pop()
        self.edited_image = self.undo_backup_image
        self.update_edited_figure()

    def action_see_history_triggered(self):
        print('****History****')
        for modifier in self.my_history:
            print(modifier)

    def action_save_in_doc_triggered(self):
        # TODO: Faze ele salvar todas as imagens do historico num arquivo .doc
        self.edited_image_fig.savefig('edited_image.png')
        self.statusbar.show()
        self.statusbar.showMessage('imagem salva', 1000)

    def about(self):
        QMessageBox.about(
            self.centralwidget,
            "About",
            """     Medical Images App
    Italo Fernandes e Ronaldo Sena escreveram este código,
ele é livre para o uso, alterações e distribuição,
se de alguma maneira ele foi útil a você, agradeça com um café, ou uma cerveja.
    Mais informações: https://github.com/ronaldosena/imagens-medicas-2""")

    # endregion
    # endregion

    # region Update Figures
    def update_original_figure(self):
        if self.original_image.dtype == np.float64:
            min_value = min(self.original_image.ravel())
            max_value = max(self.original_image.ravel())
        else:
            min_value = np.iinfo(self.original_image.dtype).min
            max_value = np.iinfo(self.original_image.dtype).max
        self.original_image_fig.gca().imshow(
            self.original_image, cmap=plt.cm.gray, clim=(min_value, max_value))
        self.original_image_fig.gca().set_title('Original Image')
        self.original_image_canvas.draw()

    def update_edited_figure_image(self, min_value, max_value,
                                   title='Edited Image', img=None):
        if img is None:
            img = self.edited_image
        im = self.edited_image_fig.gca().imshow(
            img, cmap=plt.cm.gray, clim=(min_value, max_value))
        self.edited_image_fig.gca().set_title(title)
        return im

    def update_edited_figure_hist(self, im, min_value, max_value, img=None):
        if img is None:
            img = self.edited_image
        self.edited_image_fig.gca().hist(
            img.ravel(), bins=256, range=(min_value, max_value), normed=True)
        self.edited_image_fig.colorbar(im, orientation='horizontal')

    def update_edited_figure(self):
        self.edited_image_fig.clear()
        if self.radio_compare.isChecked():
            if self.original_image.dtype == np.float64:
                o_min_value = min(self.original_image.ravel())
                o_max_value = max(self.original_image.ravel())
            else:
                o_min_value = np.iinfo(self.original_image.dtype).min
                o_max_value = np.iinfo(self.original_image.dtype).max
            self.edited_image_fig.add_subplot(1 + self.radio_hist.isChecked(), 2, 1)
            im_original = self.update_edited_figure_image(o_min_value, o_max_value,
                                                          title='Original Image',
                                                          img=self.original_image)
            if self.radio_hist.isChecked():
                self.edited_image_fig.add_subplot(2, 2, 3)
                self.update_edited_figure_hist(im_original, o_min_value, o_max_value, img=self.original_image)

        if self.edited_image.dtype == np.float64:
            min_value = min(self.edited_image.ravel())
            max_value = max(self.edited_image.ravel())
        else:
            min_value = np.iinfo(self.edited_image.dtype).min
            max_value = np.iinfo(self.edited_image.dtype).max

        if self.radio_hist.isChecked() or self.radio_compare.isChecked():
            self.edited_image_fig.add_subplot(1 + self.radio_hist.isChecked(),
                                              1 + self.radio_compare.isChecked(),
                                              1 + self.radio_compare.isChecked())

        im = self.update_edited_figure_image(min_value, max_value)

        if self.radio_hist.isChecked():
            self.edited_image_fig.add_subplot(2,
                                              1 +
                                              self.radio_compare.isChecked(),
                                              2 +
                                              2 * self.radio_compare.isChecked())
            self.update_edited_figure_hist(im, min_value, max_value)

        self.edited_image_canvas.draw()

    # endregion

    def apply_modifier(self, modifier):
        self.actionUndo.setEnabled(True)
        self.undo_backup_image = self.edited_image

        self.edited_image = modifier.apply_modifier(self.edited_image)

        self.my_history.append(modifier)
        self.statusbar.showMessage(str(modifier), 2000)
        self.update_edited_figure()

    def closeEvent(self, q_close_event):
        super(self.__class__, self).closeEvent(q_close_event)


def main():
    app = QApplication(sys.argv)
    form = IM2APP()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
