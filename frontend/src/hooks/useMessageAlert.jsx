import { useState, useCallback } from 'react';

/**
 * A custom hook for managing message state and display
 * @param {number} defaultDuration - Default time in ms before message auto-clears
 * @returns {Object} - Message state and functions
 */
const useMessageAlert = (defaultDuration = 3000) => {
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [timeoutId, setTimeoutId] = useState(null);

  // Clear any existing timeout when component unmounts or before setting a new one
  const clearExistingTimeout = useCallback(() => {
    if (timeoutId) {
      clearTimeout(timeoutId);
      setTimeoutId(null);
    }
  }, [timeoutId]);

  // Clear the message and its associated timeout
  const clearMessage = useCallback(() => {
    clearExistingTimeout();
    setMessage('');
    setMessageType('');
  }, [clearExistingTimeout]);

  // Show a message with optional type and duration
  const showMessage = useCallback((text, type = 'success', duration = defaultDuration) => {
    clearExistingTimeout(); // Clear any existing timeout
    
    setMessage(text);
    setMessageType(type);
    
    // Set up automatic clearing if duration > 0
    if (duration > 0) {
      const id = setTimeout(() => {
        clearMessage();
      }, duration);
      setTimeoutId(id);
    }
  }, [clearExistingTimeout, clearMessage, defaultDuration]);

  return {
    message,
    messageType,
    showMessage,
    clearMessage
  };
};

export default useMessageAlert;