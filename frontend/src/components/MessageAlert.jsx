import React, { useEffect } from 'react';

const MessageAlert = ({ message, messageType, onClear, autoClose = true, duration = 3000 }) => {
  useEffect(() => {
    if (message && autoClose) {
      const timer = setTimeout(() => {
        onClear();
      }, duration);
      
      return () => clearTimeout(timer);
    }
  }, [message, onClear, autoClose, duration]);

  if (!message) return null;

  const styles = {
    container: {
      padding: '10px',
      marginBottom: '15px',
      borderRadius: '4px',
      backgroundColor: messageType === 'success' ? '#d4edda' : '#f8d7da',
      color: messageType === 'success' ? '#155724' : '#721c24',
      border: `1px solid ${messageType === 'success' ? '#c3e6cb' : '#f5c6cb'}`,
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    closeButton: {
      background: 'none',
      border: 'none',
      cursor: 'pointer',
      fontSize: '16px',
      fontWeight: 'bold',
      color: messageType === 'success' ? '#155724' : '#721c24',
    }
  };

  return (
    <div style={styles.container} className={`message-alert ${messageType}`}>
      <span>{message}</span>
      <button style={styles.closeButton} onClick={onClear}>×</button>
    </div>
  );
};

export default MessageAlert;