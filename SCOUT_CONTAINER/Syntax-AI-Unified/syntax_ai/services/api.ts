// src/services/api.ts
import { BootloaderMode, Chipset, DeviceSpecs, RecoveryStrategy } from './types';

export const fetchDeviceSpecs = async (): Promise<DeviceSpecs> => {
  // Simulate fetching data from an API
  return {
    chipset: 'Qualcomm',
    powerState: 'On',
    bootloaderStatus: 'Unlocked',
  };
};

export const fetchRecoveryStrategies = async (deviceSpecs: DeviceSpecs): Promise<RecoveryStrategy> => {
  // Simulate fetching data from an API based on device specs
  return {
    hardware: {
      emmcChipExtraction: {
        temperature: '300-320°C',
        technique: 'Circular Motion',
        timing: '45-60 seconds',
        tools: ['Hot Air Rework Station', 'Ceramic Tweezers', 'eMMC Reader'],
      },
      ramPreservation: {
        keyInsight: 'Encryption keys in volatile memory if device has power',
        procedure: 'Maintain power during extraction to preserve live system state',
        window: '2-5 minutes after disassembly start',
        goal: 'Capture decrypted state before memory refresh cycle loss',
      },
      powerSequencing: {
        vcc: '3.3V apply first',
        vccq: '1.8V apply second',
        critical: 'Wrong order fries interface controller',
      },
    },
    software: {
      bootloaderModes: [
        'adb reboot bootloader',
        'adb reboot recovery',
        'adb reboot download',
        'adb reboot edl',
        'adb reboot sp',
        'adb reboot combi',
      ],
      tools: [
        'ADB Fastboot Android SDK',
        'QPST/QFIL (Qualcomm)',
        'SP Flash Tool (MediaTek)',
        'Odin (Samsung)',
      ],
      dataExtraction: [
        'dd full image',
        'foremost file carving',
        'photorec recovery',
        'sqlite3 database reconstruction',
        'binwalk partition analysis',
      ],
    },
  };
};
2. Refactor the TechnicalView Component
// src/components/TechnicalView.tsx
import React, { useState, useEffect } from 'react';
import { fetchDeviceSpecs, fetchRecoveryStrategies } from '../services/api';
import { DeviceSpecs, RecoveryStrategy } from '../types';
import { FilterIcon, ChipIcon } from './Icons';

const TechnicalView: React.FC = () => {
  const [deviceSpecs, setDeviceSpecs] = useState<DeviceSpecs>({
    chipset: '',
    powerState: '',
    bootloaderStatus: '',
  });
  const [recoveryStrategy, setRecoveryStrategy] = useState<RecoveryStrategy | null>(null);

  useEffect(() => {
    const getDeviceSpecs = async () => {
      const specs = await fetchDeviceSpecs();
      setDeviceSpecs(specs);
      const strategy = await fetchRecoveryStrategies(specs);
      setRecoveryStrategy(strategy);
    };

    getDeviceSpecs();
  }, []);

  const handleChipsetChange = (chipset: string) => {
    setDeviceSpecs({ ...deviceSpecs, chipset });
  };

  const handlePowerStateChange = (powerState: string) => {
    setDeviceSpecs({ ...deviceSpecs, powerState });
  };

  const handleBootloaderStatusChange = (bootloaderStatus: string) => {
    setDeviceSpecs({ ...deviceSpecs, bootloaderStatus });
  };

  return (
    <div className="technical-view">
      <h1>Technical Protocols</h1>
      <div className="filter-panel">
        <h2>Filter by Device Specifications</h2>
        <div className="filter-group">
          <label>
            Chipset:
            <select onChange={(e) => handleChipsetChange(e.target.value)}>
              <option value="">Select Chipset</option>
              <option value="Qualcomm">Qualcomm</option>
              <option value="MediaTek">MediaTek</option>
              <option value="Exynos">Exynos</option>
            </select>
          </label>
          <label>
            Power State:
            <select onChange={(e) => handlePowerStateChange(e.target.value)}>
              <option value="">Select Power State</option>
              <option value="On">On</option>
              <option value="Off">Off</option>
            </select>
          </label>
          <label>
            Bootloader Status:
            <select onChange={(e) => handleBootloaderStatusChange(e.target.value)}>
              <option value="">Select Bootloader Status</option>
              <option value="Unlocked">Unlocked</option>
              <option value="Locked">Locked</option>
            </select>
          </label>
        </div>
      </div>
      <div className="recovery-strategy">
        {recoveryStrategy ? (
          <>
            <h2>Recovery Strategy</h2>
            <div className="strategy-section">
              <h3>Hardware Recovery</h3>
              <p><strong>eMMC Chip Extraction:</strong> {recoveryStrategy.hardware.emmcChipExtraction.technique}</p>
              <p><strong>Temperature:</strong> {recoveryStrategy.hardware.emmcChipExtraction.temperature}</p>
              <p><strong>Timing:</strong> {recoveryStrategy.hardware.emmcChipExtraction.timing}</p>
              <p><strong>Tools:</strong> {recoveryStrategy.hardware.emmcChipExtraction.tools.join(', ')}</p>
              <p><strong>Ram Preservation:</strong> {recoveryStrategy.hardware.ramPreservation.keyInsight}</p>
              <p><strong>Procedure:</strong> {recoveryStrategy.hardware.ramPreservation.procedure}</p>
              <p><strong>Window:</strong> {recoveryStrategy.hardware.ramPreservation.window}</p>
              <p><strong>Goal:</strong> {recoveryStrategy.hardware.ramPreservation.goal}</p>
              <p><strong>Power Sequencing:</strong> {recoveryStrategy.hardware.powerSequencing.vcc} and {recoveryStrategy.hardware.powerSequencing.vccq}</p>
            </div>
            <div className="strategy-section">
              <h3>Software Exploits</h3>
              <p><strong>Bootloader Modes:</strong> {recoveryStrategy.software.bootloaderModes.join(', ')}</p>
              <p><strong>Tools:</strong> {recoveryStrategy.software.tools.join(', ')}</p>
              <p><strong>Data Extraction:</strong> {recoveryStrategy.software.dataExtraction.join(', ')}</p>
            </div>
          </>
        ) : (
          <p>Loading recovery strategy...</p>
        )}
      </div>
    </div>
  );
};

export default TechnicalView;
3. Update TypeScript Types
// src/types.ts
export interface DeviceSpecs {
  chipset: string;
  powerState: string;
  bootloaderStatus: string;
}

export interface EmMcChipExtraction {
  temperature: string;
  technique: string;
  timing: string;
  tools: string[];
}

export interface RamPreservation {
  keyInsight: string;
  procedure: string;
  window: string;
  goal: string;
}

export interface PowerSequencing {
  vcc: string;
  vccq: string;
  critical: string;
}

export interface Hardware {
  emmcChipExtraction: EmMcChipExtraction;
  ramPreservation: RamPreservation;
  powerSequencing: PowerSequencing;
}

export interface BootloaderMode {
  name: string;
  command: string;
}

export interface Software {
  bootloaderModes: string[];
  tools: string[];
  dataExtraction: string[];
}

export interface RecoveryStrategy {
  hardware: Hardware;
  software: Software;
}
4. Refactor the Data Context
// src/data/context.ts
import React, { createContext, useContext, useState } from 'react';
import { fetchDeviceSpecs, fetchRecoveryStrategies } from '../services/api';
import { DeviceSpecs, RecoveryStrategy } from '../types';

interface DataContextType {
  deviceSpecs: DeviceSpecs;
  recoveryStrategy: RecoveryStrategy | null;
  setDeviceSpecs: (specs: DeviceSpecs) => void;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export const useData = () => {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};

export const DataProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [deviceSpecs, setDeviceSpecs] = useState<DeviceSpecs>({
    chipset: '',
    powerState: '',
    bootloaderStatus: '',
  });
  const [recoveryStrategy, setRecoveryStrategy] = useState<RecoveryStrategy | null>(null);

  useEffect(() => {
    const getDeviceSpecs = async () => {
      const specs = await fetchDeviceSpecs();
      setDeviceSpecs(specs);
      const strategy = await fetchRecoveryStrategies(specs);
      setRecoveryStrategy(strategy);
    };

    getDeviceSpecs();
  }, []);

  return (
    <DataContext.Provider value={{ deviceSpecs, recoveryStrategy, setDeviceSpecs }}>
      {children}
    </DataContext.Provider>
  );
};