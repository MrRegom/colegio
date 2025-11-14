/**
 * DigitalPersona Fingerprint Engine JavaScript Wrapper
 * Este archivo proporciona una interfaz JavaScript para interactuar con el motor de procesamiento
 * de huellas digitales de DigitalPersona.
 */

/**
 * Clase que encapsula la funcionalidad del motor de procesamiento de huellas DigitalPersona
 */
class DPFPEngine {
    /**
     * Constructor de la clase DPFPEngine
     */
    constructor() {
        this.engine = null;
        this.isInitialized = false;
    }

    /**
     * Inicializa el motor de procesamiento de huellas
     * @returns {boolean} true si la inicialización fue exitosa, false en caso contrario
     */
    initialize() {
        try {
            // Intentar crear el objeto ActiveX para el motor de DigitalPersona
            this.engine = new ActiveXObject("DPFPEngLib.Engine");
            this.isInitialized = true;
            return true;
        } catch (e) {
            console.error("Error al inicializar el motor de huellas:", e.message);
            return false;
        }
    }

    /**
     * Verifica si dos plantillas de huella coinciden
     * @param {string} template1 - Plantilla de huella 1 (codificada en base64)
     * @param {string} template2 - Plantilla de huella 2 (codificada en base64)
     * @param {number} falseMatchProbability - Probabilidad de falsa coincidencia (0.01 = 1%)
     * @returns {boolean} true si las plantillas coinciden, false en caso contrario
     */
    verifyFingerprint(template1, template2, falseMatchProbability = 0.01) {
        if (!this.isInitialized) {
            if (!this.initialize()) {
                console.error("No se pudo inicializar el motor de huellas");
                return false;
            }
        }
        
        try {
            // Decodificar las plantillas de base64
            const binaryTemplate1 = this._base64ToBinary(template1);
            const binaryTemplate2 = this._base64ToBinary(template2);
            
            // Verificar si las plantillas coinciden
            return this.engine.VerifyFingerprint(binaryTemplate1, binaryTemplate2, falseMatchProbability);
        } catch (e) {
            console.error("Error al verificar las huellas:", e.message);
            return false;
        }
    }

    /**
     * Identifica una huella en un conjunto de plantillas
     * @param {string} template - Plantilla de huella a identificar (codificada en base64)
     * @param {Array<string>} templateArray - Array de plantillas de huellas (codificadas en base64)
     * @param {number} falseMatchProbability - Probabilidad de falsa coincidencia (0.01 = 1%)
     * @returns {number} Índice de la plantilla que coincide, o -1 si no hay coincidencia
     */
    identifyFingerprint(template, templateArray, falseMatchProbability = 0.01) {
        if (!this.isInitialized) {
            if (!this.initialize()) {
                console.error("No se pudo inicializar el motor de huellas");
                return -1;
            }
        }
        
        try {
            // Decodificar la plantilla de base64
            const binaryTemplate = this._base64ToBinary(template);
            
            // Crear un array con las plantillas binarias
            const binaryTemplateArray = templateArray.map(this._base64ToBinary);
            
            // Identificar la huella
            return this.engine.IdentifyFingerprint(binaryTemplate, binaryTemplateArray, falseMatchProbability);
        } catch (e) {
            console.error("Error al identificar la huella:", e.message);
            return -1;
        }
    }

    /**
     * Convierte una cadena base64 a formato binario
     * @param {string} base64 - Cadena codificada en base64
     * @returns {Array} Array con los bytes binarios
     * @private
     */
    _base64ToBinary(base64) {
        // Decodificar base64 a binario
        try {
            const raw = window.atob(base64);
            const binary = new Uint8Array(raw.length);
            
            for (let i = 0; i < raw.length; i++) {
                binary[i] = raw.charCodeAt(i);
            }
            
            return binary;
        } catch (e) {
            console.error("Error al decodificar la plantilla base64:", e.message);
            return new Uint8Array(0);
        }
    }

    /**
     * Convierte datos binarios a una cadena base64
     * @param {Array} binary - Array con los bytes binarios
     * @returns {string} Cadena codificada en base64
     */
    binaryToBase64(binary) {
        try {
            let raw = '';
            const bytes = new Uint8Array(binary);
            
            for (let i = 0; i < bytes.length; i++) {
                raw += String.fromCharCode(bytes[i]);
            }
            
            return window.btoa(raw);
        } catch (e) {
            console.error("Error al codificar a base64:", e.message);
            return '';
        }
    }
}

// Crear una instancia global para su uso fácil
window.dpfpEngine = new DPFPEngine(); 