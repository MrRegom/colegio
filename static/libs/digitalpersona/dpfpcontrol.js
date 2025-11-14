/**
 * DigitalPersona Fingerprint Control JavaScript Wrapper
 * Este archivo proporciona una interfaz JavaScript para interactuar con el control ActiveX de DigitalPersona
 * para lectores de huellas digitales.
 */

/**
 * Clase que encapsula la funcionalidad de control del lector de huellas DigitalPersona
 */
class DPFPControl {
    /**
     * Constructor de la clase DPFPControl
     */
    constructor() {
        this.reader = null;
        this.isInitialized = false;
        this.callbacks = {
            onComplete: null,
            onReaderError: null,
            onDeviceError: null
        };
    }

    /**
     * Inicializa el control del lector de huellas
     * @returns {boolean} true si la inicialización fue exitosa, false en caso contrario
     */
    initialize() {
        try {
            // Intentar crear el objeto ActiveX para DigitalPersona
            this.reader = new ActiveXObject("DPFPCtrlLib.Reader");
            
            // Configurar los callbacks para los eventos del lector
            const self = this;
            
            // Evento OnComplete - se dispara cuando se completa la captura de la huella
            this.reader.OnComplete = function(readerSerNum, fingerprintTemplate) {
                if (self.callbacks.onComplete) {
                    self.callbacks.onComplete(readerSerNum, fingerprintTemplate);
                }
            };
            
            // Evento OnReaderError - se dispara cuando hay un error en el lector
            this.reader.OnReaderError = function(readerSerNum, errorCode, errorMessage) {
                if (self.callbacks.onReaderError) {
                    self.callbacks.onReaderError(readerSerNum, errorCode, errorMessage);
                }
            };
            
            // Evento OnDeviceError - se dispara cuando hay un error en el dispositivo
            this.reader.OnDeviceError = function(readerSerNum, errorCode, errorMessage) {
                if (self.callbacks.onDeviceError) {
                    self.callbacks.onDeviceError(readerSerNum, errorCode, errorMessage);
                }
            };
            
            this.isInitialized = true;
            return true;
        } catch (e) {
            console.error("Error al inicializar el lector de huellas:", e.message);
            return false;
        }
    }

    /**
     * Configura el callback para el evento OnComplete
     * @param {function} callback - Función a llamar cuando se completa la captura
     */
    setOnCompleteCallback(callback) {
        this.callbacks.onComplete = callback;
    }

    /**
     * Configura el callback para el evento OnReaderError
     * @param {function} callback - Función a llamar cuando hay un error en el lector
     */
    setOnReaderErrorCallback(callback) {
        this.callbacks.onReaderError = callback;
    }

    /**
     * Configura el callback para el evento OnDeviceError
     * @param {function} callback - Función a llamar cuando hay un error en el dispositivo
     */
    setOnDeviceErrorCallback(callback) {
        this.callbacks.onDeviceError = callback;
    }

    /**
     * Inicia la captura de huella digital
     * @returns {boolean} true si se inició la captura, false en caso contrario
     */
    startCapture() {
        if (!this.isInitialized) {
            console.error("El lector no está inicializado");
            return false;
        }
        
        try {
            this.reader.StartCapture();
            return true;
        } catch (e) {
            console.error("Error al iniciar la captura:", e.message);
            return false;
        }
    }

    /**
     * Detiene la captura de huella digital
     * @returns {boolean} true si se detuvo la captura, false en caso contrario
     */
    stopCapture() {
        if (!this.isInitialized) {
            console.error("El lector no está inicializado");
            return false;
        }
        
        try {
            this.reader.StopCapture();
            return true;
        } catch (e) {
            console.error("Error al detener la captura:", e.message);
            return false;
        }
    }

    /**
     * Obtiene la lista de lectores conectados
     * @returns {Array} Array con los nombres de los lectores conectados
     */
    getReaders() {
        if (!this.isInitialized) {
            console.error("El lector no está inicializado");
            return [];
        }
        
        try {
            return this.reader.GetReaders();
        } catch (e) {
            console.error("Error al obtener la lista de lectores:", e.message);
            return [];
        }
    }
}

// Crear una instancia global para su uso fácil
window.dpfpControl = new DPFPControl(); 