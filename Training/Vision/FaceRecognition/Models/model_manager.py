import torch
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from matplotlib import pyplot as plt
import sklearn
import torchmetrics
import wandb


# Confusion matrix
class IntHandler:
    def legend_artist(self, legend, orig_handle, font_size, handle_box):
        x0, y0 = handle_box.xdescent, handle_box.ydescent
        text = plt.matplotlib.text.Text(x0, y0, str(orig_handle))
        handle_box.add_artist(text)
        return text


import torch
import wandb
import pytorch_lightning as pl
from pytorch_lightning.loggers import WandbLogger


class Model(pl.LightningModule):
    def __init__(self, loss_function, optimizer, train_test_sets: tuple,
                 hyper_params: dict):
        super().__init__()

        self.loss_function = loss_function
        self.optimizer = optimizer
        self.hyperparams = hyper_params

        self.num_partitions = 3
        self.p_m = {"train": 0, "test": 1, "val": 2}  # partition mapping

        self.in_training = True
        if train_test_sets is None:
            self.in_training = False

        self.init_model()
        if self.in_training:
            self.train_ds, self.test_ds, self.val_ds = train_test_sets

        self.accuracies = torch.nn.ModuleList([torchmetrics.classification.Accuracy(task="binary")
                                               for _ in range(self.num_partitions)])

    def init_model(self):
        pass

    def forward(self, x):
        pass

    def _common_log(self, y_hat, y, stage: str):
        if stage == "test":  # for test dataset, metrics are being measured separately with sklearn
            return
        index = self.p_m[stage]
        self.accuracies[index](y_hat, y)

    def _common_step(self, batch, batch_idx, stage: str):
        assert stage in ("train", "val", "test")
        x, y = batch

        y_hat = self(x)
        loss = self.loss_function(y_hat, y)
        self._common_log(y_hat, y, stage)

        return y_hat, y, loss

    def training_step(self, batch, batch_idx):
        stage = "train"
        outputs, labels, loss = self._common_step(batch, batch_idx, stage=stage)

        return {"loss": loss, "outputs": outputs, "labels": labels}

    def test_step(self, batch, batch_idx):
        stage = "test"
        outputs, labels, loss = self._common_step(batch, batch_idx, stage=stage)
        return {"inputs": batch, "loss": loss, "outputs": outputs, "labels": labels}

    def validation_step(self, batch, batch_idx):
        stage = "val"
        outputs, labels, loss = self._common_step(batch, batch_idx, stage=stage)
        return {"loss": loss, "outputs": outputs, "labels": labels}

    def training_epoch_end(self, outs) -> None:
        self.log('train_loss', torch.stack([out['loss'] for out in outs]).mean(), prog_bar=True)
        self.log('train_acc', self.accuracies[self.p_m["train"]].compute(), prog_bar=True)

    def validation_epoch_end(self, outs):
        self.log("val_loss", torch.stack([out['loss'] for out in outs]).mean(), prog_bar=True)
        self.log("val_acc", self.accuracies[self.p_m["val"]].compute(), prog_bar=True)

    def test_epoch_end(self, outs):
        outputs = torch.cat([tmp['outputs'] for tmp in outs])
        labels = torch.cat([tmp['labels'] for tmp in outs])
        inputs = torch.cat([tmp['inputs'][0] for tmp in outs])

        outputs_cpu = outputs.cpu().detach().numpy()
        inputs_cpu = inputs.cpu().detach().numpy()
        predictions_cpu = (outputs_cpu > 0.5).astype(int).squeeze()
        labels_cpu = labels.squeeze().tolist()

        accuracy = sklearn.metrics.accuracy_score(predictions_cpu, labels_cpu)
        balanced_accuracy = sklearn.metrics.balanced_accuracy_score(predictions_cpu, labels_cpu)
        f1 = sklearn.metrics.f1_score(predictions_cpu, labels_cpu, average="macro")

        wandb.log({"media/test_confusion_matrix": wandb.plot.confusion_matrix(preds=predictions_cpu, y_true=labels_cpu,
                                                                              class_names=["SAME", "DIFFERENT"])})
        self.log("test_accuracy", accuracy, prog_bar=True)
        self.log("test_balanced_accuracy", balanced_accuracy, prog_bar=True)
        self.log("test_f1_score", f1, prog_bar=True)

        # Each input is of a shape (2, 3, 64, 64), and is composed of two RGB images
        # Plot some examples of input images and their predictions
        for i in range(15):
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            axes[0].imshow(inputs_cpu[i][0].transpose(1, 2, 0))
            axes[1].imshow(inputs_cpu[i][1].transpose(1, 2, 0))
            axes[2].imshow(inputs_cpu[i][0].transpose(1, 2, 0))
            axes[2].imshow(inputs_cpu[i][1].transpose(1, 2, 0), alpha=0.5)
            axes[2].set_title(f"Prediction: {predictions_cpu[i]}, Label: {labels_cpu[i]}")
            wandb.log({"media/test_examples": wandb.Image(fig)})

    def configure_optimizers(self):
        return self.optimizer(self.parameters(), lr=self.hyperparams["learning_rate"])

    def train_dataloader(self):
        return DataLoader(self.train_ds, batch_size=self.hyperparams["batch_size"], shuffle=True, num_workers=0)

    def test_dataloader(self):
        return DataLoader(self.test_ds, batch_size=self.hyperparams["batch_size"], shuffle=False, num_workers=0)

    def val_dataloader(self):
        return DataLoader(self.val_ds, batch_size=self.hyperparams["batch_size"], shuffle=False, num_workers=0)
