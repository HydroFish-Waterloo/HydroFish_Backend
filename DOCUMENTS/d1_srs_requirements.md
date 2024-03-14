# (SRS) Requirement for backend


1. [from history page](#1-for-history-page)


## 1. for history page

<table>
    <tr>
        <th>input</th>
        <th>output</th>
    </tr>
    <tr>
        <td>
            <pre><code>GET http://localhost:8000/hydrofish/get_history_monthly/</code></pre>
        </td>
        <td>
            <pre><code>{
    "status": "success",
    "data": [
        {
            "day": "2024-02-13T00:00:00Z",
            "total_ml": 4328
        },
        {
            ...
        },
        {
            "day": "2024-03-14T00:00:00Z",
            "total_ml": 2062
        }
    ]
}</code></pre>
        </td>
    </tr>
</table>

