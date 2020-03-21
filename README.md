# Edge-Conditioned-Convolution
3D-CAD classification using ECC 

## For training, run:

python main.py \
--dataset modelnet10 --test_nth_epoch 10 --lr 0.1 --lr_steps '[20,40,60]' --epochs 75 --batch_size 8 --batch_parts 1 \
--model_config 'i_0.5_1, c_16,b,r, c_32,b,r, m_1.25_3.75, c_32,b,r, c_32,b,r, m_3.75_11.25, c_64,b,r, m_1e5_1e5, f_64,b,r,d_0.2,f_4' \
--fnet_llbias 0 --fnet_widths '[16,32]' --pc_augm_scale 1.2 --pc_augm_mirror_prob 0.2 --pc_augm_input_dropout 0.1 \
--nworkers 3 --edgecompaction 1 --odir results/trash

## Printing the confusion matrix for a pretrained model:

python main.py \
--dataset modelnet10 --epochs -1 --nworkers 3 --edgecompaction 1 \
--resume results/benchmark_files_vertices/model.pth.tar --odir results/benchmark_files_vertices_cm

