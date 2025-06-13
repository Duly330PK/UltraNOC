import React from "react";

const DWDMConfigPanel = () => {
  return (
    <div className="p-4 bg-nocgray rounded-2xl shadow">
      <h2 className="text-xl font-semibold text-nocblue mb-2">DWDM-Konfiguration</h2>
      <form>
        <label className="block mb-2">
          Kanalanzahl:
          <input type="number" className="w-full mt-1 p-2 rounded bg-gray-800 text-white" />
        </label>
        <label className="block mb-2">
          Wellenlänge (nm):
          <input type="text" className="w-full mt-1 p-2 rounded bg-gray-800 text-white" />
        </label>
        <button type="submit" className="mt-4 bg-nocblue text-white px-4 py-2 rounded">
          Speichern
        </button>
      </form>
    </div>
  );
};

export default DWDMConfigPanel;