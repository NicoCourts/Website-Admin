const {app, BrowserWindow, ipcMain, dialog} = require('electron')
const fs = require('fs')
const RSA = require('node-rsa')
const windowStateKeeper = require('electron-window-state')

// Keep global references to all the windows
global.windows = {}
// Change API url whenever we want!
global.baseURL = 'https://api.nicocourts.com/'
// global.baseURL = 'http://localhost:8080/'

const createWindow = () => {
  // Create the window states for the visible windows
  const mainWinState = windowStateKeeper({
    file: 'main.json',
    defaultWidth: 800,
    defaultHeight: 600,
  })
  const previewWinState = windowStateKeeper({
    file: 'preview.json',
    defaultWidth: 800,
    defaultHeight: 600,
  })
  const editorWinState = windowStateKeeper({
    file: 'editor.json',
    defaultWidth: 800,
    defaultHeight: 600,
  })
  const imageWinState = windowStateKeeper({
    file: 'images.json',
    defaultWidth: 800,
    defaultHeight: 600,
  })

  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: mainWinState.width,
    height: mainWinState.height,
    x: mainWinState.x,
    y: mainWinState.y,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
    },
  })
  mainWinState.manage(mainWindow)
  global.windows['main'] = mainWindow

  // Create preview window (hidden at first)
  const previewWindow = new BrowserWindow({
    width: previewWinState.width,
    height: previewWinState.height,
    x: previewWinState.x,
    y: previewWinState.y,
    show: false,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
    },
  })
  previewWinState.manage(previewWindow)
  previewWindow.loadURL(`file://${__dirname}/preview.html`)
  global.windows['preview'] = previewWindow

  // Create Editor Window
  const editorWindow = new BrowserWindow({
    width: editorWinState.width,
    height: editorWinState.height,
    x: editorWinState.x,
    y: editorWinState.y,
    show: false,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
    },
  })
  editorWinState.manage(editorWindow)
  editorWindow.loadURL(`file://${__dirname}/post-edit.html`)
  global.windows['editor'] = editorWindow

  // Create image Window
  const imageWindow = new BrowserWindow({
    width: imageWinState.width,
    height: imageWinState.height,
    x: imageWinState.x,
    y: imageWinState.y,
    show: false,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
    },
  })
  imageWinState.manage(imageWindow)
  imageWindow.loadURL(`file://${__dirname}/photos.html`)
  global.windows['image'] = imageWindow

  // Create interface window (hidden at first)
  const interfaceWindow = new BrowserWindow({
    width: 800,
    height: 600,
    show: false,
    webPreferences: {
      nodeIntegration: true,
    },
  })
  interfaceWindow.loadURL(`file://${__dirname}/interface.html`)
  global.windows['interface'] = interfaceWindow

  // Populate posts
  interfaceWindow.webContents.on('did-finish-load', () => {
    interfaceWindow.webContents.send('get-all-posts')
  })

  // and load the index.html of the app.
  mainWindow.loadURL(`file://${__dirname}/index.html`)

  // Emitted when the window is closed.
  mainWindow.on('closed', () => {
    // If the main window is closed we're donezo
    app.quit()
  })
}

// This provides a method for signing requests
ipcMain.on('sign-blob', (event, blob) => {
  fs.readFile('/etc/pki/privkey.pem', (err, data) => {
    if (err) throw err
    const key = new RSA(data)
    key.setOptions({'signingScheme': 'pkcs1-sha512'})
    event.returnValue = key.sign(blob)
  })
})

// Handle Dialogs!
ipcMain.on('open-dialog', (_event, head, body) => {
  const options = {
    type: 'info',
    title: head,
    message: body,
    buttons: ['Ok'],
  }
  dialog.showMessageBox(options)
})
ipcMain.on('open-image-dialog', (event) => {
  dialog.showOpenDialog({
    properties: ['openFile'],
    message: "Choose an image to upload."
  }, (files) => {
    if (files) {
      event.sender.send('selected-directory', files)
    }
  })
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // I am not running MacOS
  app.quit()
})
