import React, { useState, useEffect, useRef } from 'react';

const TerminalTab = ({ element }) => {
    const [output, setOutput] = useState([]);
    const [input, setInput] = useState('');
    const [history, setHistory] = useState([]);
    const [historyIndex, setHistoryIndex] = useState(-1);
    const endOfMessagesRef = useRef(null);
    const inputRef = useRef(null);
    const [isFetching, setIsFetching] = useState(false);

    const scrollToBottom = () => endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });

    useEffect(scrollToBottom, [output]);

    useEffect(() => {
        setOutput([`Verbunden mit ${element.properties.label} (${element.properties.id}).`]);
        setInput('');
        setHistory([]);
        setHistoryIndex(-1);
        inputRef.current?.focus();
    }, [element.properties.id]);

    const handleCommand = async (e) => {
        if (e.key === 'Enter' && input.trim() !== '' && !isFetching) {
            const command = input.trim();
            if (command) setHistory(prev => [command, ...prev]);
            setHistoryIndex(-1);

            const prompt = `<span class="text-noc-green">${element.properties.label}></span> ${command}`;
            setOutput(prev => [...prev, prompt]);
            setInput('');
            setIsFetching(true);

            const token = localStorage.getItem('ultranoc_token');
            try {
                const response = await fetch(`/api/v1/simulation/devices/${element.properties.id}/action`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify({ type: 'get_cli_output', payload: { command } }),
                });
                const data = await response.json();
                setOutput(prev => [...prev, data.output.replace(/\n/g, '<br/>')]);
            } catch (error) {
                setOutput(prev => [...prev, `<span class="text-noc-red">Fehler bei der Befehlsausführung.</span>`]);
            } finally {
                setIsFetching(false);
            }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (history.length > 0) {
                const newIndex = Math.min(history.length - 1, historyIndex + 1);
                setHistoryIndex(newIndex);
                setInput(history[newIndex] || '');
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex > 0) {
                const newIndex = historyIndex - 1;
                setHistoryIndex(newIndex);
                setInput(history[newIndex] || '');
            } else {
                setHistoryIndex(-1);
                setInput('');
            }
        }
    };

    useEffect(() => {
        if (!isFetching) {
            inputRef.current?.focus();
        }
    }, [isFetching]);

    return (
        <div className="h-full flex flex-col font-mono text-sm">
            <div className="flex-grow bg-noc-dark p-2 rounded-t-md overflow-y-auto whitespace-pre-wrap border border-noc-border" onClick={() => inputRef.current?.focus()}>
                {output.map((line, index) => <div key={index} dangerouslySetInnerHTML={{ __html: line }} />)}
                <div ref={endOfMessagesRef} />
            </div>
            <div className="flex bg-noc-dark p-2 rounded-b-md border-x border-b border-noc-border">
                {/* KORREKTUR: Das '>' Zeichen muss innerhalb des Strings sein, um als Text behandelt zu werden. */}
                <span className="text-noc-green">{element.properties.label}></span>
                <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleCommand}
                    className="bg-transparent border-none outline-none text-noc-text flex-grow ml-2"
                    disabled={isFetching}
                    autoFocus
                />
            </div>
        </div>
    );
};

export default TerminalTab;