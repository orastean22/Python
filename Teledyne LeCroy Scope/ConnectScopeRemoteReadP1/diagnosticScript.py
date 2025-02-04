import pyvisa as visa

# Configuration - Update these values based on your scope
SCOPE_IP = "10.30.11.37"  # Use the IP that works in ping
PORT = 5025  # Default SCPI port, change if different
CONNECTION_STRING = f"TCPIP::{SCOPE_IP}::{PORT}::SOCKET"

def run_diagnostics():
    rm = visa.ResourceManager()
    print(f"VISA Backend: {rm}")
    
    try:
        # List all available resources
        resources = rm.list_resources()
        print("\nDetected VISA Resources:")
        for i, res in enumerate(resources, 1):
            print(f"{i}. {res}")
            
        # Try explicit connection
        print(f"\nAttempting connection to: {CONNECTION_STRING}")
        scope = rm.open_resource(CONNECTION_STRING)
        scope.timeout = 3000  # 3 second timeout
        
        # Test basic communication
        idn = scope.query("*IDN?")
        print(f"\n*IDN? Response: {idn.strip()}")
        
        scope.close()
        
    except visa.VisaIOError as e:
        print(f"\nVISA Error [{e.error_code}]: {e.description}")
        if e.error_code == visa.constants.VI_ERROR_RSRC_NFOUND:
            print("Possible solutions:")
            print("1. Check VISA driver installation")
            print("2. Verify LXI/VXI-11 is enabled on the scope")
            print("3. Try different connection string format")
    except Exception as e:
        print(f"\nGeneral error: {str(e)}")
    finally:
        rm.close()

if __name__ == "__main__":
    run_diagnostics()