## Conitnuous ArrowKey

### Problem

- vscode on Mac does not work for continuous arrow key when using Vim
- the below command on terminal makes it work

### Solution

```
defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false
```
